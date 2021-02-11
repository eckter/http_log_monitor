from collections import defaultdict
from typing import List, Dict, Tuple
from log_monitor.models import LogEntry


def _section_from_entry(entry: LogEntry) -> str:
    request = entry.request
    resource = request.split()[1]
    return "/".join(resource.split("/", 2)[:2])


def _get_hits_per_section(entries: List[LogEntry]) -> Dict[str, int]:
    hits_per_section = defaultdict(lambda: 0)
    for entry in entries:
        section = _section_from_entry(entry)
        hits_per_section[section] += 1
    return dict(hits_per_section)


def _section_most_hit(entries: List[LogEntry]) -> Tuple[str, int]:
    hits_per_section = _get_hits_per_section(entries)
    section, n_hits = max(hits_per_section.items(), key=lambda x: x[1])
    hit_percent = (100 * n_hits) // len(entries)
    return section, hit_percent


def print_most_hit(entries: List[LogEntry], _: float):
    if not entries:
        return
    section, hit_percent = _section_most_hit(entries)
    print(f"Section with most hits: {section} ({hit_percent}%)")
