import imghdr
from io import StringIO
import json
import operator
import os

import arrow
import click
from flask.cli import with_appcontext
from PIL import Image
import requests
from sqlalchemy_searchable import search as vector_search
from tabulate import tabulate
from unstdlib.standard.functools_ import memoized

from . import create_app
from .models import Application, Collection, File, get_db, TableBase
from .util import sha256_file

from multiprocessing.pool import ThreadPool


_REQUESTS_SESSION = None


def _download_images(shot_source, shot_dir):
    global _REQUESTS_SESSION
    os.mkdir(shot_dir)
    if not _REQUESTS_SESSION:
        _REQUESTS_SESSION = requests.Session()

    # TODO: this should be a list comprehension,
    # but the nested bit doesn't work?
    links = []
    for obj in shot_source:
        for link in obj.values():
            links.append(link)

    f_objs = []
    for idx, link in enumerate(links):
        response = _REQUESTS_SESSION.get(link)
        content_type = response.headers.get('Content-Type', None)
        if content_type and content_type[0:6] == 'image/':
            ext = content_type[6:]
        else:
            continue

        sio = StringIO()
        sio.write(response.content)
        img = Image(sio)
        w, h = img.size

        filename = '{}_{}x{}'.format(idx, w, h)
        img.save(filename, ext)


@memoized
def _get_or_create_collection_obj(session, name, type='category'):
    """Get a collection object from the database or create a new
    one from the provided options, defaulting the others.

    NOTE: Calls flush to populate a collection's id in the case that
    a new object is created, but does not call commit"""

    q = session.query(Collection).filter(Collection.name == name,
                                         Collection.type == type)
    coll = q.first()
    if not coll:
        coll = Collection(
            name=name,
            type=type,
            featured=False)
        session.flush()
    return coll


def _load_file(filename):
    with open(filename) as f:
        contents = json.load(f)
        return contents['data'][0]


def _resolve_source(ctx, param, value):
    if not value:
        if os.path.isdir('data/'):
            click.echo('==> No source provided')
            click.echo('==> Folder ./data/ exists. Assuming that is our source'
                       ' folder...')
            return os.path.realpath('data/')
        else:
            raise click.BadParameter('Cannot find a suitable source directory.'
                                     ' Please specify one with --source / -s')
    return value


def process_downloads(path, content):
    image_dir = os.path.join(path, 'images')
    if os.path.isdir(image_dir):
        return
    os.mkdir(image_dir)

    for source in ['screenshot', 'header', 'list', 'icon']:
        source_dir = os.path.join(image_dir, '{}s'.format(source))
        if os.path.isdir(source_dir):
            click.echo('==> Found {} directory for {}, not overwriting'.format(
                source, content['title']))
            continue

        source_ary = content.get('{}_images'.format(source), None)
        if not source_ary:
            source_obj = content.get('{}_image'.format(source), None)
            source_ary = [source_obj] if source_obj else None

        if source_ary:
            _download_images(app_guid, source_ary, source_dir)


def _populate_tags(session):
    for tag in ['Face', 'Tools & Utilities', 'Game',
                'Health & Fitness', 'Remote', 'Notification',
                'Daily', 'Index', 'GetSomeApps']:
        tag_obj = Tag(name=tag)
        session.add(tag_obj)
    return session


def _create_file_obj(fullpath, file_type):
    w = None
    h = None
    sha256 = sha256_file(fullpath)

    try:
        img = Image.open(fullpath)
        w, h = img.size
    except IOError:
        # file isn't an image
        pass

    file_obj = File(type=file_type,
                    path=fullpath,
                    image_width=w,
                    image_height=h,
                    sha256=sha256)

    return file_obj


def _load_json_file(session, path, pbw_path=None):
    contents = _load_file(path)
    create_ts = arrow.get(contents['created_at'])
    category_name = contents['category_name']
    category = _get_or_create_collection_obj(
        session, name=category_name)

    try:
        publish_ts = arrow.get(contents['published_date'])
    except KeyError:
        publish_ts = None

    click.echo('==> Adding {}...'.format(contents['title']))
    app = Application(guid=contents['uuid'],
                      author=contents['author'],
                      title=contents['title'],
                      description=contents['description'],
                      source=contents['source'],
                      create_ts=create_ts,
                      publish_ts=publish_ts,
                      collections=[category],
                      hearts=contents['hearts'])
    session.add(app)
    session.flush()

    # TODO: Screenshots etc.
    if pbw_path:
        pbw = File(application_id=app.id,
                   type='pbw',
                   path=pbw_path)
        session.add(pbw)

    return app, path, contents


@click.command()
@click.option('--source', type=click.Path(exists=True,
                                          file_okay=False,
                                          dir_okay=True,
                                          resolve_path=True),
              callback=_resolve_source)
@with_appcontext
def getimgs(source):
    _get_images(source)


def _get_images(source):
    results = []

    pool = ThreadPool(processes=10)
    for path, _, files in os.walk(source):
        for f in files:
            if f.endswith('.json') and not f.startswith('.#'):
                fullpath = os.path.join(path, f)
                content = _load_file(fullpath)
                results.append(pool.apply_async(process_downloads,
                                                args=(path, content)))
    pool.close()
    pool.join()


@click.command()
@click.option('--source', type=click.Path(exists=True,
                                          file_okay=False,
                                          dir_okay=True,
                                          resolve_path=True),
              callback=_resolve_source)
@with_appcontext
def populatedb(source):
    import pebble_store
    _get_images(source)

    app = pebble_store.create_app()
    # download_results = []
    # pool = ThreadPool(processes=10)
    Session, db = get_db()

    TableBase.metadata.drop_all(db)
    TableBase.metadata.create_all(db, checkfirst=True)

    session = Session()
    for path, _, files in os.walk(source):
        json_files = [f for f in files
                      if f.endswith('.json') and not f.startswith('.#')
                      for f in files]
        pbw_files = [f for f in files if f.endswith('.pbw')]

        if json_files and pbw_files:
            # We're looking at a valid application directory
            # TODO: Maybe handle multiple files?
            f = json_files[0]
            fullpath = os.path.join(path, f)
            app, fullpath, contents = _load_json_file(session, fullpath,
                                                      pbw_path=pbw_files[0])

    session.commit()


@click.command()
@click.argument('search', nargs=-1)
@with_appcontext
def search(search):
    session, db = get_db()
    search = ' '.join(search)

    query = session.query(Application)
    query = vector_search(query, search)

    to_print = []
    for result in query:
        to_print.append((result.title,
                         [x.name for x in result.collections],
                         result.author,
                         result.hearts))
    to_print.sort(key=operator.itemgetter(-1))
    click.echo(tabulate(to_print, tablefmt='fancy_grid'))


@click.command()
@click.option('--port', '-p', default=5000, type=int)
@click.option('--host', '-h', default='0.0.0.0')
def run(port, host):
    """Run a development server"""
    app = create_app()
    app.run(host=host, port=port)
