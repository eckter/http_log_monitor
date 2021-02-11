from datetime import datetime
import pytest

from log_monitor.models import LogEntry


def test_log_entry__valid():
    log_txt = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'
    entry = LogEntry(log_txt)
    assert entry.host == "127.0.0.1"
    assert entry.identity == "-"
    assert entry.user_id == "james"
    assert entry.time_str == "[09/May/2018:16:00:39 +0000]"
    assert entry.time == datetime(2018, 5, 9, 16, 0, 39)
    assert entry.timezone == "+0000"
    assert entry.request == '"GET /report HTTP/1.0"'
    assert entry.status == 200
    assert entry.size == 123


def test_log_entry__missing_quote():
    log_txt = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0 200 123'
    with pytest.raises(RuntimeError):
        LogEntry(log_txt)


def test_log_entry__missing_field():
    log_txt = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0 200'
    with pytest.raises(RuntimeError):
        LogEntry(log_txt)
