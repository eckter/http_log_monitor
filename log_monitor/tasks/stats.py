from .task import Task
from datetime import datetime
from log_monitor.tasks import stat_modules
from log_monitor.models import LogEntry
from typing import List


class Stats(Task):
    def __init__(self, configs: dict):
        super().__init__(configs.get("delay", 10))
        self.entries = []
        self.begin = datetime.now()
        self.stat_modules = []
        self._load_modules(configs.get("modules", []))

    def _load_modules(self, modules_list: List[str]):
        for module in modules_list:
            self.stat_modules.append(getattr(stat_modules, module))

    def _on_timer(self):
        end = datetime.now()
        time_elapsed = (end - self.begin).total_seconds()
        print(f"Statistics from {self.begin} to {end}:")
        for module in self.stat_modules:
            module(self.entries, time_elapsed)
        self.entries = []
        self.begin = end

    def register_entry(self, entry: LogEntry):
        self.entries.append(entry)
