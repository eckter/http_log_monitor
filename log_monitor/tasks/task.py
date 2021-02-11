import time
from log_monitor.models import LogEntry


class Task:
    """
    Tasks are objects that watch for new log entries, and run actions at a specified interval
    They are managed by the Runner class
    """
    def __init__(self, interval: float):
        self.interval = interval
        self.next_timer = time.time() + interval

    def update(self) -> None:
        """
        This method is called regularly by Runner, and calls _on_timer when the timer has elapsed
        """
        if time.time() > self.next_timer:
            self.next_timer += self.interval
            self._on_timer()

    def _on_timer(self) -> None:
        """
        This is the method called on a timer, to be overwritten with inheritance
        """
        pass

    def register_entry(self, entry: LogEntry):
        """
        This method is called whenever a new entry is written to the file
        to be overwritten with inheritance
        :param entry: new log entry
        """
        pass
