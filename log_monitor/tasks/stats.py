from .task import Task
from datetime import datetime
from log_monitor.tasks import stat_modules
from log_monitor.models import LogEntry
from typing import List


class Stats(Task):
    """
    This class regroups all the stat modules, to be displayed every 10 seconds (configurable)

    Modules are functions in the stat_modules directory, they take as parameter a list of entries for the interval
    as well as the interval length in seconds

    The configuration dict is expected to be as follow:
        config["update_interval"]: duration (s) between each update, defaults to 10
        config["modules"]: list of module names to be loaded in stat_modules
    """
    def __init__(self, configs: dict):
        """
        :param configs: config dictionary
        """
        super().__init__(configs.get("update_interval", 10))
        self.entries = []
        self.begin = datetime.now()
        self.stat_modules = []
        self._load_modules(configs.get("modules", []))

    def _load_modules(self, modules_list: List[str]) -> None:
        """
        Loads all the modules specified in the config file
        :param modules_list: list of module names
        """
        for module in modules_list:
            self.stat_modules.append(getattr(stat_modules, module))

    def _on_timer(self) -> None:
        """
        Called every {config["delay"]} seconds, display stats
        """
        end = datetime.now()
        time_elapsed = (end - self.begin).total_seconds()
        print(f"\n\nStatistics from {self.begin} to {end}:")
        for module in self.stat_modules:
            module(self.entries, time_elapsed)
        print(flush=True)
        self.entries = []
        self.begin = end

    def register_entry(self, entry: LogEntry) -> None:
        """
        Register a new log entry

        They are stored in a list to be forwarded to each module
        :param entry: new log entry
        """
        self.entries.append(entry)
