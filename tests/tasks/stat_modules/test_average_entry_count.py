from log_monitor.tasks.stat_modules.average_entry_count import _compute_average_entry_count


def test_average_entry_count():
    entries = ["entry1", "entry2", "entry3"]
    time = 6
    assert _compute_average_entry_count(entries, time) == 0.5
