import hashlib
from urllib.parse import unquote

import click
from flask import url_for

from . import create_app


def sha256_file(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def list_routes(app):
    app = create_app()
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = unquote('{:50s} {:20s} {}'.format(
            rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        click.echo(line)
