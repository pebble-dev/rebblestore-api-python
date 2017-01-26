from setuptools import setup

setup(
    name='Pebble Store',
    version='0.1',
    long_description=__doc__,
    packages=['rebble_store'],
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
            'populatedb=rebble_store.cli:populatedb',
            'search=rebble_store.cli:search',
            'run=rebble_store.cli:run',
            'list_routes=rebble_store.cli:list_routes',
        ],
    }
)
