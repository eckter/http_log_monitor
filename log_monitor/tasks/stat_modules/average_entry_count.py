from typing import List
from log_monitor.models import LogEntry


def _compute_average_entry_count(entries: List[LogEntry], interval_duration: float) -> float:
    """
    Computes the average entry per second, in an interval of {interval_duration} seconds
    :param entries: list of entries registered in the interval
    :param interval_duration: length of the interval
    :return: average entry per second
    """
    return len(entries) / interval_duration


def average_entry_count(entries: List[LogEntry], interval_duration: float):
    """
    Prints the average log entry per second in the interval
    :param entries: list of entries registered in the interval
    :param interval_duration: length of the interval
    """
    average = _compute_average_entry_count(entries, interval_duration)
    average = round(average, 2)
    print("Average log entry per second: ", average)
