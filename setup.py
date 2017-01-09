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
                      'pillow',
                      'psycopg2',
                      'requests',
                      'sqlalchemy',
                      'sqlalchemy-searchable',
                      'sqlalchemy-utils',
                      'tabulate'],
    entry_points={
        'flask.commands': [
            'populatedb=pebble_store.cli:populatedb',
            'search=pebble_store.cli:search',
            'run=pebble_store.cli:run'
        ],
    }
)
