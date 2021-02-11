from .task import Task
from collections import deque
from datetime import datetime
from time import time
from log_monitor.models import LogEntry


class Alerts(Task):
    """
    This class manages the detection and reporting of alerts

    It detects when the average number of requests per seconds excess a threshold
    this is done using a queue of request times, removing a request when it falls outside of the interval
    and watching when the length of the queue reaches the threshold

    When the program has been running for less that {average_over} seconds, it checks the average since start time
    so that if we average over 10 minutes, and the first few seconds are way beyond the threshold, we report the
    alert immediately

    The configuration dict is expected to be as follow:
        config["update_time"]: duration (s) between each update where we look for end of alert, defaults to 1
        config["average_over"]: duration over which we average the requests per seconds, defaults to 120
        config["request_frequency_threshold"]: request / second threshold, defaults to 10
    """
    def __init__(self, configs: dict):
        """
        :param configs: config dictionary
        """
        super().__init__(configs.get("update_time", 1))
        self.average_over = configs.get("average_over", 120)
        self.threshold_per_sec = configs.get("request_frequency_threshold", 10)
        self.entry_times = deque()
        self.is_alert = False
        self.begin_alert = None
        self.start_time = time()

        assert self.average_over > 0, "average duration must be positive"

    def _remove_old_elements(self) -> None:
        """
        Removes any element from the queue that is too old to be included in the average
        """
        while self.entry_times:
            last_element = self.entry_times.popleft()
            still_in_interval = last_element >= time() - self.average_over
            if still_in_interval:
                self.entry_times.appendleft(last_element)
                return

    def _on_timer(self) -> None:
        """
        Called once every {config["update_time"]} seconds. We check for end of alert mode here
        """
        self._check_alert_end()

    def _check_alert_end(self) -> None:
        """
        Checks for the end of alert mode, printing a message once it's over
        """
        self._remove_old_elements()
        if self.is_alert and not self._is_over_threshold(len(self.entry_times)):
            duration = (datetime.now() - self.begin_alert).total_seconds()
            print(f"Alert: recovered at {datetime.now()}, after {duration}s")
            self.is_alert = False

    def _actual_average_duration(self) -> float:
        """
        Computes how long is the interval we're averaging over

        It may be shorter when the program started recently
        :return: duration in seconds
        """
        begin_average = time() - self.average_over
        begin_run = self.start_time
        if begin_average < begin_run:
            return max(1., time() - begin_run)
        else:
            return self.average_over

    def _is_over_threshold(self, n_entries: int) -> bool:
        """
        Checks if n entries in the queue is over the threshold
        :param n_entries: number of registered entries
        :return: true if it is over
        """
        entries_per_sec = n_entries / self._actual_average_duration()
        return entries_per_sec > self.threshold_per_sec

    def _check_alert_begin(self) -> None:
        """
        Checks if we enter alert mode
        """
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

    def register_entry(self, entry: LogEntry):
        """
        Registers a new entry, adds it to the queue and looks for beginning of alert
        :param entry: new log entry
        """
        self.entry_times.append(time())
        self._check_alert_begin()
