from setuptools import setup

setup(
    name='Pebble Store',
    version='0.1',
    long_description=__doc__,
    packages=['pebble_store'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['arrow',
                      'click',
                      'Flask',
                      'flask-restful',
                      'pillow',
                      'psycopg2',
                      'requests',
                      'sqlalchemy',
                      'sqlalchemy-searchable',
                      'sqlalchemy-utils',
                      'tabulate',
                      'webargs'],
    entry_points={
        'flask.commands': [
            'populatedb=pebble_store.cli:populatedb',
            'search=pebble_store.cli:search',
            'run=pebble_store.cli:run',
            'list_routes=pebble_store.cli:list_routes',
        ],
    }
)
