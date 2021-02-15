from log_monitor.runner import Runner
from log_monitor.models import LogEntry
from mock import patch


tmp_file = "./tmp"
base_entry_txt = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'
base_entry_txt_2 = '127.0.0.1 - toto [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'


def _base_conf() -> dict:
    conf_dict = {
        "log_file": tmp_file,
        "tasks": {
            "Stats": {1: 1}
        }
    }
    return conf_dict


@patch("log_monitor.tasks.Stats.register_entry")
@patch("log_monitor.tasks.task.Task.register_old_entry")
def test_runner__read_new_lines(mock_register_old_entry, mock_register_entry):
    conf_dict = _base_conf()
    with open(tmp_file, "w") as f:
        runner = Runner(conf_dict)
        print(base_entry_txt, file=f)
        print(base_entry_txt_2, file=f, flush=True)
    res1 = runner._read_new_entries(False)
    res2 = runner._read_new_entries(False)
    assert res1 is True
    assert res2 is False
    mock_register_entry.assert_any_call(LogEntry(base_entry_txt))
    mock_register_entry.assert_called_with(LogEntry(base_entry_txt_2))
    mock_register_old_entry.assert_not_called()


@patch("log_monitor.tasks.Stats.register_entry")
@patch("log_monitor.tasks.task.Task.register_old_entry")
def test_runner__read_existing_lines(mock_register_old_entry, mock_register_entry):
    conf_dict = _base_conf()
    with open(tmp_file, "w") as f:
        print(base_entry_txt, file=f)
        print(base_entry_txt_2, file=f, flush=True)
        runner = Runner(conf_dict)
    res1 = runner._read_new_entries(False)
    assert res1 is False
    mock_register_old_entry.assert_any_call(LogEntry(base_entry_txt))
    mock_register_old_entry.assert_called_with(LogEntry(base_entry_txt_2))
    mock_register_entry.assert_not_called()


@patch("log_monitor.tasks.Stats")
def test_runner__init_tasks(mock_stats):
    conf_dict = _base_conf()
    with open(tmp_file, "w"):
        Runner(conf_dict)
    mock_stats.assert_called_with({1: 1})


@patch("log_monitor.tasks.Stats.register_entry")
def test_runner__register_entry(mock_register_entry):
    conf_dict = _base_conf()
    with open(tmp_file, "w"):
        runner = Runner(conf_dict)
    log_txt = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'
    runner._register_entry(log_txt, False)
    call = mock_register_entry.call_args_list[0]
    assert type(call.args[0]) is LogEntry
    assert call.args[0].status == 200


@patch("log_monitor.tasks.task.Task.update")
def test_runner__call_update(mock_update):
    conf_dict = _base_conf()
    with open(tmp_file, "w"):
        runner = Runner(conf_dict)
    runner._update_all_tasks()
    mock_update.assert_called()
