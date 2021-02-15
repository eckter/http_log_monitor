from log_monitor.tasks.stat_modules.average_entry_count import _compute_average_entry_count
from log_monitor.models import LogEntry


def test_average_entry_count():
    entries = [LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123')] * 3
    time = 6
    assert _compute_average_entry_count(entries, time) == 0.5
