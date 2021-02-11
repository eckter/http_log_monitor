from log_monitor.tasks import Stats
from log_monitor.models import LogEntry
from mock import patch


@patch("log_monitor.tasks.stat_modules.average_entry_count")
def test_stats__modules_call(mock_average_entry_count):
    stats = Stats({
        "modules": ["average_entry_count"]
    })
    stats._on_timer()
    mock_average_entry_count.assert_called()


@patch("log_monitor.tasks.stat_modules.average_entry_count")
def test_stats__modules_forward_entries(mock_average_entry_count):
    stats = Stats({
        "modules": ["average_entry_count"]
    })
    log_txt = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'
    entry = LogEntry(log_txt)
    stats.register_entry(entry)
    stats._on_timer()
    call = mock_average_entry_count.call_args_list[0]
    assert call.args[0] == [entry]


@patch("log_monitor.tasks.stat_modules.average_entry_count")
def test_stats__clear_entries(mock_average_entry_count):
    stats = Stats({
        "modules": ["average_entry_count"]
    })
    log_txt = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'
    entry = LogEntry(log_txt)
    stats.register_entry(entry)
    stats._on_timer()
    stats._on_timer()
    call = mock_average_entry_count.call_args_list[1]
    assert call.args[0] == []
