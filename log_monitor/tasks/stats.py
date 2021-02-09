from .task import Task
import time
from log_monitor.tasks import stat_modules


class Stats(Task):
    def __init__(self, configs):
        super().__init__(configs["delay"])
        self.entries = []
        self.begin = time.time()
        self.stat_modules = []
        self.load_modules(configs["modules"])

    def load_modules(self, modules_list):
        for module in modules_list:
            self.stat_modules.append(getattr(stat_modules, module))

    def _on_timer(self):
        end = time.time()
        time_elapsed = end - self.begin
        print(f"Statistics from {self.begin} to {end}:")
        for module in self.stat_modules:
            module(self.entries, time_elapsed)
        self.entries = []
        self.begin = end

    def register_entry(self, entry):
        self.entries.append(entry)
