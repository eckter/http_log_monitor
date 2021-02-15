from collections import defaultdict
from typing import List, Dict, Tuple
from log_monitor.models import LogEntry


def _section_from_entry(entry: LogEntry) -> str:
    """
    Get the section from a LogEntry, as defined as "everything before the second / in the resource section"
    example: '127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234' -> "/api"
    :param entry: entry
    :return: section accessed
    """
    request = entry.request
    resource = request.split()[1]
    return "/".join(resource.split("/", 2)[:2])


def _get_hits_per_section(entries: List[LogEntry]) -> Dict[str, int]:
    """
    Counts how many times each section has been accessed
    :param entries: list of log entries
    :return: dict, with section as keys and how many times it's been accessed as value
    """
    hits_per_section = defaultdict(lambda: 0)
    for entry in entries:
        section = _section_from_entry(entry)
        hits_per_section[section] += 1
    return dict(hits_per_section)


def _section_most_hit(entries: List[LogEntry]) -> Tuple[str, int]:
    """
    Computes the section with the most hits, as well as a percentage of requests that has accessed the section
    :param entries: list of entries
    :return: (section, hit%)
    """
    hits_per_section = _get_hits_per_section(entries)
    section, n_hits = max(hits_per_section.items(), key=lambda x: x[1])
    hit_percent = (100 * n_hits) // len(entries)
    return section, hit_percent


def print_most_hit(entries: List[LogEntry], _: float) -> None:
    """
    Prints which section has received the most hits
    :param entries: list of entries
    :param _: duration of the interval, not used here
    """
    if not entries:
        return
    section, hit_percent = _section_most_hit(entries)
    print(f"Section with most hits: {section} ({hit_percent}%)")
