def average_entry_count(entries, interval_duration):
    avg = len(entries) / interval_duration
    print("average log entry per second: ", avg)
