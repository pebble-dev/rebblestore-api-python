import operator

import click
from flask.cli import with_appcontext
from sqlalchemy_searchable import parse_search_query
from tabulate import tabulate

from ..models import Application, ft_search_vector, get_db, User

from .populate import getimgs, populatedb
from .run import run, list_routes


@click.command()
@click.argument('search', nargs=-1)
@with_appcontext
def search(search):
    session, db = get_db()
    search = ' '.join(search)

    apps = session.query(Application).join(User).filter(
        ft_search_vector.match(parse_search_query(search)))

    to_print = []
    for result in apps:
        to_print.append((result.title,
                         ', '.join([x.name for x in result.collections]),
                         result.author.name,
                         result.hearts))
    to_print.sort(key=operator.itemgetter(-1))
    click.echo(tabulate(to_print, tablefmt='fancy_grid'))


__all__ = [getimgs, populatedb, run, list_routes, search]
