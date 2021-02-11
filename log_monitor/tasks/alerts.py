from .task import Task
from collections import deque
from datetime import datetime
from time import time


class Alerts(Task):
    def __init__(self, configs):
        super().__init__(configs.get("update_time", 1))
        self.average_over = configs.get("average_over", 120)
        self.threshold_per_sec = configs.get("request_frequency_threshold", 10)
        self.entry_times = deque()
        self.is_alert = False
        self.begin_alert = None
        self.start_time = time()

        assert self.average_over > 0, "average duration must be positive"

    def _remove_old_elements(self):
        while self.entry_times:
            last_element = self.entry_times.popleft()
            still_in_interval = last_element >= time() - self.average_over
            if still_in_interval:
                self.entry_times.appendleft(last_element)
                return

    def _on_timer(self):
        self._check_alert_end()

    def _check_alert_end(self):
        self._remove_old_elements()
        if self.is_alert and not self._is_over_threshold(len(self.entry_times)):
            duration = (datetime.now() - self.begin_alert).total_seconds()
            print(f"Alert: recovered at {datetime.now()}, after {duration}s")
            self.is_alert = False

    def _actual_average_duration(self):
        begin_average = time() - self.average_over
        begin_run = self.start_time
        if begin_average < begin_run:
            return max(1., time() - begin_run)
        else:
            return self.average_over

    def _is_over_threshold(self, n_entries):
        entries_per_sec = n_entries / self._actual_average_duration()
        return entries_per_sec > self.threshold_per_sec

    def _check_alert_begin(self):
        self._remove_old_elements()
        average_duration = self._actual_average_duration()
        if not self.is_alert and self._is_over_threshold(len(self.entry_times)):
            self.is_alert = True
            self.begin_alert = datetime.now()
            average_per_second = len(self.entry_times) / self.average_over
            msg = f"Alert: at {datetime.now()}\n" + \
                f"Average requests per second in the " + \
                f"last {average_duration}s went over the threshold of " + \
                f"{self.threshold_per_sec} (currently at {average_per_second}/s)"
            print(msg)

    def register_entry(self, entry):
        self.entry_times.append(time())
        self._check_alert_begin()

