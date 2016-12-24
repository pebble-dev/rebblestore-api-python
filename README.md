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


[reddit_archive]: https://www.reddit.com/r/pebble/comments/5g0gmx/in_light_of_recent_news_i_archived_the_app_store/
[pebble_dev]: https://github.com/pebble-dev
[rebble_store]: https://github.com/pebble-dev/rebble-store