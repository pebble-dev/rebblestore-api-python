import json
import os

import arrow
import click
from flask.cli import with_appcontext
import requests
from sqlalchemy_searchable import search as vector_search

from . import create_app
from .models import Application, get_db, PebbleCategory, TableBase

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

    for idx, link in enumerate(links):
        response = _REQUESTS_SESSION.get(link)
        content_type = response.headers.get('Content-Type', None)
        if content_type and content_type[0:6] == 'image/':
            ext = content_type[6:]
        else:
            continue
        filename = '{}.{}'.format(str(idx), ext)
        save_path = os.path.join(shot_dir, filename)
        with open(save_path, 'wb') as f:
            click.echo('==> Writing {}'.format(save_path))
            f.write(response.content)


def _load_file(filename):
    with open(filename) as f:
        contents = json.load(f)
        return contents['data'][0]


def _resolve_source(ctx, param, value):
    if not value:
        if os.path.isdir('data/'):
            click.echo('==> No source provided')
            click.echo('==> Folder ./data/ exists. Assuming that is our source folder...')
            return os.path.realpath('data/')
        else:
            raise click.BadParameter('Cannot find a suitable source directory. Please specify one with --source / -s')
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
            _download_images(source_ary, source_dir)


@click.command()
@click.option('--source', type=click.Path(exists=True,
                                          file_okay=False,
                                          dir_okay=True,
                                          resolve_path=True),
              callback=_resolve_source)
@click.option('-d', '--drop_old', is_flag=True)
@click.option('--no_download', is_flag=True, default=False)
@with_appcontext
def initdb(source, drop_old, no_download):
    """Instantiate the DB"""
    download = not no_download
    download_results = []

    process_pool = None
    if download:
        process_pool = ThreadPool(processes=10)

    import pebble_store
    app = pebble_store.create_app()
    session, db = get_db()

    if drop_old:
        TableBase.metadata.drop_all(db)
        TableBase.metadata.create_all(db, checkfirst=True)

    for path, _, files in os.walk(source):
        for f in files:
            # TODO: this error checking could be made more robust
            if f.endswith('.json') and not f.startswith('.#'):
                fullpath = os.path.join(path, f)
                contents = _load_file(fullpath)
                category = PebbleCategory.get_by_value(
                    contents['category_name'])
                create_ts = arrow.get(contents['created_at']).datetime
                try:
                    publish_ts = arrow.get(contents['published_date']).datetime
                except KeyError:
                    publish_ts = None

                if download:
                    download_results.append(
                        process_pool.apply_async(
                            process_downloads,
                            args=(path, contents)))

                click.echo('==> Adding {}...'.format(contents['title']))
                app = Application(guid=contents['uuid'],
                                  author=contents['author'],
                                  title=contents['title'],
                                  description=contents['description'],
                                  source=contents['source'],
                                  category=category,
                                  create_ts=create_ts,
                                  publish_ts=publish_ts,
                                  hearts=contents['hearts']
                )
                session.add(app)
    click.echo('==> Committing session...')
    if download:
        click.echo('==> Waiting for pool to finish work')
        process_pool.close()
        process_pool.join()
    session.commit()


@click.command()
@click.argument('search', nargs=-1)
@with_appcontext
def search(search):
    session, db = get_db()
    search = ' '.join(search)

    query = session.query(Application)
    query = vector_search(query, search)
    for result in query:
        click.echo('==> {} ({}) {}'.format(result.title,
                                            result.category.value,
                                            result.author))


@click.command()
@click.option('--port', '-p', default=5000, type=int)
@click.option('--host', '-h', default='0.0.0.0')
def run(port, host):
    """Run a development server"""
    app = create_app()
    app.run(host=host, port=port)
