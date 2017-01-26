import os

import click
from flask.cli import with_appcontext

from .. import create_app, util


@click.command()
@click.option('--port', '-p', default=5000, type=int)
@click.option('--host', '-h', default='0.0.0.0')
@click.option('--config', '-c',
              type=click.Path(exists=True, file_okay=True, resolve_path=False))
def run(port, host, config):
    """Run a development server"""
    if config:
        config = os.path.abspath(os.path.expanduser(config))
    else:
        config = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              '..',
                              'app_debug.cfg')

    app = create_app(config=config)
    # with app.app_context():
    #     util.list_routes(app)
    app.run(host=host, port=port)


@click.command()
@with_appcontext
def list_routes():
    app = create_app()
    util.list_routes(app)
