from collections import defaultdict


def section_from_entry(entry):
    request = entry.request
    resource = request.split()[1]
    return "/".join(resource.split("/", 2)[:2])


def get_hits_per_section(entries):
    hits_per_section = defaultdict(lambda: 0)
    for entry in entries:
        section = section_from_entry(entry)
        hits_per_section[section] += 1
    return dict(hits_per_section)


def section_most_hit(entries):
    hits_per_section = get_hits_per_section(entries)
    section, n_hits = max(hits_per_section.items(), key=lambda x: x[1])
    hit_percent = (100 * n_hits) // len(entries)
    return section, hit_percent


def print_most_hit(entries, _):
    if not entries:
        return
    section, hit_percent = section_most_hit(entries)
    print(f"Section with most hits: {section} ({hit_percent}%)")

