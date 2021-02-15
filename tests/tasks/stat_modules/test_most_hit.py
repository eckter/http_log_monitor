from log_monitor.tasks.stat_modules.most_hit import _section_from_entry, _section_most_hit, _get_hits_per_section
from log_monitor.models import LogEntry
import pytest


base_entry = LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123')
base_entries = [
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'),
    LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /api HTTP/1.0" 200 123'),
]


@pytest.mark.parametrize("request_txt,section", [
    ('"GET /report HTTP/1.0"', "/report"),
    ('"GET /report/ HTTP/1.0"', "/report"),
    ('"GET /report/foo HTTP/1.0"', "/report"),
    ('"GET /foo/bar HTTP/1.0"', "/foo"),
    ('"POST /foo/bar HTTP/42.0"', "/foo"),
    ('"POST /foo/bar/toto/foo HTTP/42.0"', "/foo"),
    ('"POST foo HTTP/42.0"', "foo"),
])
def test_section_from_entry(request_txt, section):
    entry = base_entry
    print(entry.request)
    entry.request = request_txt
    assert _section_from_entry(entry) == section


def test_get_hits_per_section():
    result = _get_hits_per_section(base_entries)
    assert result == {
        "/report": 2,
        "/api": 1
    }


def test_section_most_hit():
    section, percent = _section_most_hit(base_entries)
    assert section == "/report"
    assert percent == 66
