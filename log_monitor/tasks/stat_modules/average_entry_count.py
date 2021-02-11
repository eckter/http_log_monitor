def _compute_average_entry_count(entries, interval_duration):
    return len(entries) / interval_duration


def average_entry_count(entries, interval_duration):
    average = _compute_average_entry_count(entries, interval_duration)
    print("average log entry per second: ", average)
