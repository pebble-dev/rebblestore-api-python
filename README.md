# DEPRECATED: NO LONGER UNDER ACTIVE DEVELOPMENT.
Due to lack of time and lack of desire to compete for resources with the [other implementation][https://github.com/pebble-dev/rebblestore-api], we are no longer updating this repository. Please have a look at the Golang repository if you wish to make contributions to the rebblestore api effort. 

# Rebble Store Python API .
This is a Python implementation of the Rebble Store api.

If you want to contribute join us on the [Pebble Dev Discord server](http://discord.gg/aRUAYFN), then head to `#appstore`.

## Usage

### Installation
First, you'll need Python > 3. I recommend the latest stable (3.6.0 as of this writing).
You can install this either through [pyenv][pyenv], your OS's package manager, or by compiling from source.

Next you'll need PostgreSQL. This should be installed via your OS's package manager if possible.
If not, you may install from source.

You'll need a `pebble` user (with password `pebble`) and a database to which this user has full rights (called `pebble_app`) running on the same machine as the server running this project.
These values are all overwritable by building a proper config. This is explained below.

Once a python 3.x binary is in your `$PATH` and PostgreSQL is running with the above mentioned user, password, and database, you should be able to install with pip:

```bash
git clone https://github.com/pebble-dev/rebblestore-api-python/
cd rebblestore-api-python
pip install .
```

*N.B:* If you intend to develop on this project `pip install -e .` may be more appropriate, as this installs the project 'editably'.
See `pip install -h` for more information on this functionality.

### Configuration

Some application behavior is overridable via a config file.
The default implementation for a debug server is at [rebble_store/app_debug.cfg](rebble_store/app_debug.cfg).

This config file may be either edited directly (**NOT** recommended) or copied and then passed as the argument `--config` option when running `flask run`.

Currently the following behavior is overridable from this file:

* PostgreSQL configuration:

    - Host
    - Database
    - Username
    - Password

* Server Name (This only affects the `list_routes` flask cli helper currently)


### Functionality

Once the package has been installed, you may easily run the development server. In the same directory you changed into above, run:

```bash
export FLASK_APP=run.py
flask run
```

This will start the development server at [localhost:5000][dev_server] and begin responding to requests.
Once `FLASK_APP` has been set (as above), you may inspect these additional commands with `flask`.

Additionly, there are a number of commands intended to assist in populating the earlier mentioned PostgreSQL database with data.
These commands presume that a "source" directory exists on the hard disk somewhere in the same format as is downloadable [here][store_clone].

*N.B:* This functionality has not been tested throughly enough for my liking.
It seems to work for us, but please open an issue (or better yet - a pull request) yshould you encounter any issues.

## License
Unless otherwise specified within the header in a specific file, the AGPLv3 license applies to every file within the containing repository.

[pyenv]:http://github.com/yyuu/pyenv
[dev_server]:http://localhost:5000
[store_clone]:https://www.reddit.com/r/pebble/comments/5g0gmx/in_light_of_recent_news_i_archived_the_app_store/
