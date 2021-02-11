from typing import List
from log_monitor.models import LogEntry


def _compute_average_entry_count(entries: List[LogEntry], interval_duration: float) -> float:
    return len(entries) / interval_duration


def average_entry_count(entries: List[LogEntry], interval_duration: float):
    average = _compute_average_entry_count(entries, interval_duration)
    print("average log entry per second: ", average)
