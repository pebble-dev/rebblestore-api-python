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
                      'sqlalchemy',
                      'sqlalchemy-searchable',
                      'psycopg2']
)
