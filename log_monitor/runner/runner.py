import sys
import time
from ..models import LogEntry


class Runner:
    """
    This class manages running all the tasks and watching for file updates
    """
    def __init__(self, config_dict):
        # TODO fill tasks
        self.tasks = []
        self.watched_file = open(config_dict["log_file"], "r")
        self.watched_file.seek(0, 2)    # skip to the end of file

    def _register_entry(self, log_entry):
        for task in self.tasks:
            task.register_entry(log_entry)

    def run(self):
        while True:
            new_text = self.watched_file.read()
            if new_text:
                for entry_txt in new_text.split("\n"):
                    try:
                        entry = LogEntry(entry_txt)
                        self._register_entry(entry)
                    except RuntimeError:
                        print("error: invalid log entry:", entry_txt, file=sys.stderr)
            else:
                time.sleep(0.1)
