from setuptools import setup

setup(
    name='Pebble Store',
    version='0.1',
    long_description=__doc__,
    packages=['pebble_store'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask',
                      'arrow',
                      'click',
                      'requests',
                      'sqlalchemy',
                      'sqlalchemy-searchable',
                      'tabulate',
                      'psycopg2',
                      'pillow'],
    entry_points={
        'flask.commands': [
            'initdb=pebble_store.cli:initdb',
            'search=pebble_store.cli:search',
            'run=pebble_store.cli:run'
        ],
    }
)
