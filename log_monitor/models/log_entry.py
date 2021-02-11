from clfparser import CLFParser
from typing import Dict


class LogEntry:
    """
    Represents the content of an entry following Common Log Format
    """
    def __init__(self, string_entry: str):
        try:
            entry_dict = CLFParser.logDict(string_entry)
        except ValueError:
            raise RuntimeError("Invalid log entry")

        if not self._is_valid(entry_dict):
            raise RuntimeError("Invalid log entry")

        self.host = entry_dict["h"]
        self.identity = entry_dict["l"]
        self.user_id = entry_dict["u"]
        self.time_str = entry_dict["t"]
        self.time = entry_dict["time"]
        self.timezone = entry_dict["timezone"]
        self.request = entry_dict["r"]
        self.status = int(entry_dict["s"])
        self.size = int(entry_dict["b"])
        self.referer = entry_dict["Referer"]
        self.user_agent = entry_dict["Useragent"]

    @staticmethod
    def _is_valid(entry_dict: Dict[str, str]) -> bool:
        for v in entry_dict.values():
            if v:
                return True
        return False
