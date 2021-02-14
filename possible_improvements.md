Possible improvements:

* Better handling of timestamps: I relied on the time of writing when applicable,
it would be more reliable to use the timestamps in the log.
* Improve tests: I have mostly written unit tests, I could use more of
integration/system/other tests.
And we never have too many tests
* More stat modules, using the rest of the info in the log files, eg:
  * Userid stats, who sends the most requests
  * IP stats, same as above
  * Size of the objects, maybe with the userid/ip
  * More detailed error reporting: server error per section,
  client error per userid
* Possibly lighten up the genericity of the tasks module: I made it easy to add new tasks,
but for two classes (stats and alerts) it may be too much.
* Build a docker image for easier deployment, although a python module is
already easy enough.
