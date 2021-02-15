from log_monitor.tasks.stat_modules.error_reporting import _get_client_error_stats, _get_error_stats, \
    _get_server_error_stats, _is_server_error, _is_client_error
from log_monitor.models import LogEntry
import pytest


entries = [
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 100 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 101 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 201 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 300 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 301 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 400 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 401 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 500 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 501 123'),
]


@pytest.mark.parametrize("entry,expected", zip(entries, [
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    True,
    False,
    False,
]))
def test_is_client_error(entry, expected):
    assert _is_client_error(entry) == expected


@pytest.mark.parametrize("entry,expected", zip(entries, [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    True,
]))
def test_is_server_error(entry, expected):
    assert _is_server_error(entry) == expected


def test_get_error_stats():
    n, percent = _get_error_stats([], _is_server_error)
    assert n == 0, percent == 0


def test_get_server_error_stats():
    n, percent = _get_server_error_stats(entries)
    assert n == 2, percent == 20


def test_get_client_error_stats():
    n, percent = _get_client_error_stats(entries)
    assert n == 2, percent == 20
