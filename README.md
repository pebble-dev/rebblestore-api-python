# Pebble Store Replacement

## Introduction
Short story first: My wife bought me a Pebble Steel this Christmas.
Literally days before the news of the FitBit buyout dropped.
This kind of sucks, as there's no guarantee that the Pebble Store will remain open past 2017.

However, then I found [this Reddit post][reddit_archive], in which /u/magmapus describes his archiving of the current Pebble store.
I downloaded this and imagined users running a personal version of the Pebble store and performing full-text queries against a running database.
I didn't forsee being able to run this publicly, as there are some issues with licensing of all of the uploaded faces and apps.

This is the result of that idea.

## Progress
So far we have:

* A command to index the current database into a running PostgreSQL instance (see the `initdb` command)
* A page to search over the full-text fields
* A *VERY* basic page which allows viewing of a single app (no screenshots, no download link, just metadata)

## Related projects
After starting this project, I found out that [pebble_dev] are working on the [Rebble store][rebble_store]. They're following a
"modern" web development model and are separating the UI from the API, which I'm not sure that I find appealing (it's all the same application after all).


## License
Like much of my work, this project is available under a 3-clause BSD license.
Unless otherwise specified within the header in a specific file, the license below applies to every file within the containing repository.

Copyright (c) 2016, Bryan Bennett
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


[reddit_archive]: https://www.reddit.com/r/pebble/comments/5g0gmx/in_light_of_recent_news_i_archived_the_app_store/
[pebble_dev]: https://github.com/pebble-dev
[rebble_store]: https://github.com/pebble-dev/rebble-store