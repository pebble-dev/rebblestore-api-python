import json
import os

import arrow
import click
from flask import abort, Flask, g, render_template, request
from sqlalchemy_searchable import search as vector_search

from .models import Application, get_connection, PebbleCategory, TableBase


def get_db():
    """get the connection to the db, but cache it on the g object"""
    if not hasattr(g, 'db'):
        g.db = get_connection()
    return g.db[0], g.db[1]


app = Flask(__name__)


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


@app.cli.command()
@click.option('--source', type=click.Path(exists=True,
                                          file_okay=False,
                                          dir_okay=True,
                                          resolve_path=True),
              callback=_resolve_source)
@click.option('-d', '--drop_old', is_flag=True)
def initdb(source, drop_old):
    """Instantiate the DB"""
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
                click.echo('Adding {}...'.format(contents['uuid']))
                app = Application(guid=contents['uuid'],
                                  author=contents['author'],
                                  title=contents['title'],
                                  description=contents['description'],
                                  source=contents['source'],
                                  category=category,
                                  create_ts=create_ts,
                                  publish_ts=publish_ts)
                session.add(app)
    click.echo('Committing session...')
    session.commit()



@app.cli.command()
@click.argument('search', nargs=-1)
def search(search):
    session, db = get_db()
    search = ' '.join(search)

    query = session.query(Application)
    query = vector_search(query, search)
    for result in query:
        click.echo('{} ({}) {}'.format(result.title,
                                       result.category,
                                       result.author))


@app.teardown_appcontext
def shutdown_session(response_or_exception):
    if hasattr(g, 'db'):
        g.db[0].close()
    return response_or_exception


@app.route('/')
def render_root():
    session, db = get_db()
    search_string = request.args.get('q', None)
    if not search_string:
        search_string = ''
    query = session.query(Application)
    query = vector_search(query, search_string)

    return render_template('index.html', results=query, query=search_string)


@app.route('/<guid>')
def render_app_page(guid):
    # TODO: error handling here (ensure guid is a guid)
    session, db = get_db()

    app = session.query(Application).filter(Application.guid == guid).first()
    if not app:
        abort(404)

    return render_template('app.html', app=app)


def create_app():
    app = Flask(__name__)
    return app
