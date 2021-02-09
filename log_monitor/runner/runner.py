import importlib
import sys
import time
from ..models import LogEntry
from ..tasks import Stats


class Runner:
    """
    This class manages running all the tasks and watching for file updates
    """
    def __init__(self, config_dict):
        self.tasks = []
        self.watched_file = open(config_dict["log_file"], "r")
        self.watched_file.seek(0, 2)    # skip to the end of file

        self.tasks.append(Stats(config_dict["tasks"]["stats"]))

    def _register_entry(self, log_entry):
        for task in self.tasks:
            task.register_entry(log_entry)

    def _update_all_tasks(self):
        for task in self.tasks:
            task.update()

    def _read_new_entries(self):
        new_text = self.watched_file.read()
        if new_text:
            for entry_txt in new_text.split("\n"):
                if entry_txt:
                    try:
                        entry = LogEntry(entry_txt)
                        self._register_entry(entry)
                    except RuntimeError:
                        print("error: invalid log entry:", entry_txt, file=sys.stderr)
        return len(new_text) > 0

    def run(self):
        while True:
            if not self._read_new_entries():
                time.sleep(0.1)
            self._update_all_tasks()
