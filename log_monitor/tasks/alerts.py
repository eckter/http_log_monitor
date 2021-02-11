from .task import Task
from collections import deque
from datetime import datetime
from time import time


class Alerts(Task):
    def __init__(self, configs):
        super().__init__(configs["update_time"])
        self.average_over = configs.get("average_over", 120)
        self.threshold_per_sec = configs.get("request_frequency_threshold", 10)
        self.threshold = self.threshold_per_sec * self.average_over
        self.entry_times = deque()
        self.is_over_threshold = False
        self.begin_alert = None

    def _remove_old_elements(self):
        while self.entry_times:
            last_element = self.entry_times.popleft()
            still_in_interval = last_element >= time() - self.average_over
            if still_in_interval:
                self.entry_times.appendleft(last_element)
                return

    def _on_timer(self):
        self._remove_old_elements()
        self._check_alert_end()

    def _check_alert_end(self):
        if self.is_over_threshold and len(self.entry_times) < self.threshold:
            duration = (datetime.now() - self.begin_alert).total_seconds()
            print(f"Alert: recovered at {datetime.now()}, after {duration}s")
            self.is_over_threshold = False

    def _check_alert_begin(self):
        if not self.is_over_threshold and len(self.entry_times) > self.threshold:
            self.is_over_threshold = True
            self.begin_alert = datetime.now()
            average_per_second = len(self.entry_times) / self.average_over
            msg = f"Alert: at {datetime.now()}\n" + \
                f"Average requests per second in the " + \
                f"last {self.average_over}s went over the threshold of " + \
                f"{self.threshold_per_sec} (currently at {average_per_second}/s)"
            print(msg)

    def register_entry(self, entry):
        self.entry_times.append(time())
        self._check_alert_begin()

