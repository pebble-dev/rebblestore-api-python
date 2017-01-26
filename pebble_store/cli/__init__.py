import operator

import click
from flask.cli import with_appcontext
from sqlalchemy_searchable import search as vector_search
from tabulate import tabulate

from ..models import Application, get_db

from .populate import getimgs, populatedb
from .run import run, list_routes


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


__all__ = [getimgs, populatedb, run, list_routes, search]
