from log_monitor.tasks import Alerts
from log_monitor.models import LogEntry
from mock import patch
from freezegun import freeze_time


tmp_file = "./tmp"
base_entry = LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123')


def _make_config(average_over=120., threshold=10., update_time=1.):
    return {
        "average_over": average_over,
        "request_frequency_threshold": threshold,
        "update_time": update_time
    }


@patch("log_monitor.tasks.alerts.time")
def test_alerts__remove_old_elements(mock_time):
    mock_time.return_value = 0
    conf_dict = _make_config(average_over=1)
    alerts = Alerts(conf_dict)
    alerts._remove_old_elements()

    alerts.register_entry(base_entry)
    mock_time.return_value = 0.5
    alerts.register_entry(base_entry)
    mock_time.return_value = 1.5
    alerts.register_entry(base_entry)
    mock_time.return_value = 2
    alerts._remove_old_elements()
    assert len(alerts.entry_times) == 1


@patch("log_monitor.tasks.alerts.time")
def test_alerts__check_alert_begin(mock_time):
    conf_dict = _make_config(average_over=10, threshold=10)
    mock_time.return_value = 0
    alerts = Alerts(conf_dict)
    mock_time.return_value = 20
    for _ in range(30):
        alerts.register_entry(base_entry)
    alerts._on_timer()
    assert not alerts.is_alert
    # 30 over 10s

    mock_time.return_value = 26
    for _ in range(30):
        alerts.register_entry(base_entry)
    alerts._on_timer()
    assert not alerts.is_alert
    # 60 over 10s

    mock_time.return_value = 32
    # first are removed, 30 over 10s

    for _ in range(60):
        alerts.register_entry(base_entry)
    alerts._on_timer()
    assert not alerts.is_alert
    # 90 over 10s

    mock_time.return_value = 33
    for _ in range(20):
        alerts.register_entry(base_entry)
    # 110 over 10s, above threshold
    alerts._on_timer()
    assert alerts.is_alert


@patch("log_monitor.tasks.alerts.time")
def test_alerts__check_alert_end(mock_time):
    conf_dict = _make_config(average_over=10, threshold=10)
    mock_time.return_value = 0
    alerts = Alerts(conf_dict)
    mock_time.return_value = 20
    for _ in range(60):
        alerts.register_entry(base_entry)
    mock_time.return_value = 25
    for _ in range(60):
        alerts.register_entry(base_entry)
    alerts._on_timer()
    assert alerts.is_alert
    mock_time.return_value = 32
    alerts._check_alert_end()
    assert not alerts.is_alert


@freeze_time("05-09-2018 16:00:45")
@patch("log_monitor.tasks.alerts.time")
def test_alerts__check_pre_read(mock_time):
    conf_dict = _make_config(average_over=10, threshold=10)
    mock_time.return_value = 0
    alerts = Alerts(conf_dict)
    alerts.register_old_entry(base_entry)
    assert len(alerts.entry_times) > 0
    alerts._on_timer()
    assert len(alerts.entry_times) > 0
    mock_time.return_value = 5
    alerts._on_timer()
    assert len(alerts.entry_times) == 0


@freeze_time("05-09-2018 16:00:45 +0200")
@patch("log_monitor.tasks.alerts.time")
def test_alerts__check_pre_read_tz(mock_time):
    tz_diff_entry = LogEntry('127.0.0.1 - james [09/May/2018:16:00:39 +0200] "GET /report HTTP/1.0" 200 123')
    conf_dict = _make_config(average_over=10, threshold=10)
    mock_time.return_value = 0
    alerts = Alerts(conf_dict)
    alerts.register_old_entry(tz_diff_entry)
    assert len(alerts.entry_times) > 0
    alerts._on_timer()
    assert len(alerts.entry_times) > 0
    mock_time.return_value = 5
    alerts._on_timer()
    assert len(alerts.entry_times) == 0


@freeze_time("05-09-2018 16:10:45")
@patch("log_monitor.tasks.alerts.time")
def test_alerts__check_pre_read_old(mock_time):
    conf_dict = _make_config(average_over=10, threshold=10)
    mock_time.return_value = 0
    alerts = Alerts(conf_dict)
    alerts.register_old_entry(base_entry)
    assert len(alerts.entry_times) == 0
