## recruitment project: CLF log monitor

This is my implementation of a "take home project" I was given
by a company for its recruitement process.
It consists in an HTTP log monitor.

It reads a file text continuously, and displays stats and alerts.


### Installation

It works like a usual python package:
`cd` to the root directory then `python setup.py install`

For development, it is advised to create a virtual environment
(through venv, conda, or similar) and
`pip install -e .`


### Usage

Once installed, you can run the `log_monitor` command anywhere.
By default the default config is loaded, but you can also
pass a config file as parameter (ie. `log_monitor config.yml`)

By default stats will be displayed every 10 seconds, and alerts
raised when we register too many requests.

To exit, send a keyboard interrupt signal (ctrl-C)


### Config file

The configuration file is a yaml, a documented example with default values
is at the root of the project (config_default.yml).


### Tests

To run tests, run `./tests/run_tests.sh`
