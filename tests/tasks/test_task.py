from log_monitor.tasks.task import Task
from mock import patch
from time import time


@patch("log_monitor.tasks.task.Task._on_timer")
def test_task__call_update(mock_on_timer):
    task = Task(0.1)
    end_loop = time() + 0.22
    while time() < end_loop:
        task.update()
    assert len(mock_on_timer.call_args_list) == 2