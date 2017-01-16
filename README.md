# Pebble Store Replacement

This is a Python implementation of the rebble store api.

## Usage

### Installation
First, you'll need Python > 3. I recommend the latest stable (3.6.0 as of this writing).
You can install this either through [pyenv][pyenv], your OS's package manager, or by compiling from source.

Next you'll need PostgreSQL. This should be installed via your OS's package manager if possible.
If not, you may install from source.

You'll need a `pebble` user (with password `pebble`) and a database to which this user has full rights (called `pebble_app`) running on the same machine as the server running this project.
The URI, username, password and database will eventually be fully customizable, but this functionality has yet to be implemented.

Once a python 3.x binary is in your `$PATH` and PostgreSQL is running with the above mentioned user, password, and database, you should be able to install with pip:

```bash
git clone https://github.com/pebble-dev/rebblestore-api-python/
cd rebblestore-api-python
pip install .
```

*N.B:* If you intend to develop on this project `pip install -e .` may be more appropriate, as this installs the project 'editably'.
See `pip install -h` for more information on this functionality.

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
Unless otherwise specified within the header in a specific file, the license below applies to every file within the containing repository.

<pre>
Copyright (c) 2016, Rebble store developers
All rights reserved.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
</pre>

[pyenv]:http://github.com/yyuu/pyenv
[dev_server]:http://localhost:5000
[store_clone]:https://www.reddit.com/r/pebble/comments/5g0gmx/in_light_of_recent_news_i_archived_the_app_store/