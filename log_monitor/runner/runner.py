import sys
import time
from ..models import LogEntry
from log_monitor import tasks


class Runner:
    """
    This class manages running all the tasks and watching for file updates

    The configuration dict is expected to be as follow:
        config["log_file"]: path to the file to watch
        config["tasks"]: dictionary describing the tasks and their config
            keys are the name of the classes, values are their respective configuration dicts
    """
    def __init__(self, config_dict: dict):
        """
        :param config_dict: content of the config file
        """
        self.tasks = []
        self.watched_file = open(config_dict["log_file"], "r")

        task_config = config_dict.get("tasks", {})
        for class_name, conf in task_config.items():
            task = getattr(tasks, class_name)
            self.tasks.append(task(conf))
        self._read_new_entries(True)

    def _register_entry(self, entry_txt: str, old: bool) -> None:
        """
        Manages a new line written to the file, forwarding it to the tasks
        :param entry_txt: CLF string
        :param old: True if it's an entry from before startup time
        """
        try:
            entry = LogEntry(entry_txt)
            for task in self.tasks:
                if old:
                    task.register_old_entry(entry)
                else:
                    task.register_entry(entry)
        except RuntimeError:
            print("error: invalid log entry:", entry_txt, file=sys.stderr, flush=True)

    def _update_all_tasks(self) -> None:
        """
        Runs update on all tasks, running the timed events
        """
        for task in self.tasks:
            task.update()

    def _read_new_entries(self, is_first_read: bool) -> bool:
        """
        Read the file to look for new entries
        :return: True if something was written since last update
        """
        new_text = self.watched_file.read()
        if new_text:
            for entry_txt in new_text.split("\n"):
                if entry_txt:
                    self._register_entry(entry_txt, is_first_read)
        return len(new_text) > 0

    def run(self):
        """
        Runs all the tasks, watching for file update and running timed events (blocking)
        Stops on KeyboardInterrupts
        """
        while True:
            try:
                if not self._read_new_entries(False):
                    time.sleep(0.1)
                self._update_all_tasks()
            except KeyboardInterrupt:
                break
