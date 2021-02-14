from datetime import datetime
from clfparser import CLFParser
from typing import Dict
from datetime import timezone


class LogEntry:
    """
    Represents the content of an entry following Common Log Format
    """
    def __init__(self, string_entry: str):
        """
        Create the object given the log entry as a string in Common Log Format
        On error, raises a RuntimeError

        Note: timezone is automatically converted to UTC
        :param string_entry: CLF string
        """
        try:
            entry_dict = CLFParser.logDict(string_entry)
        except ValueError:  # raised when the date format is invalid
            raise RuntimeError("Invalid log entry")
        if not self._is_valid(entry_dict):
            raise RuntimeError("Invalid log entry")

        self.host = entry_dict["h"]
        self.identity = entry_dict["l"]
        self.user_id = entry_dict["u"]
        self.request = entry_dict["r"]
        self.status = int(entry_dict["s"])
        self.size = int(entry_dict["b"])
        self.referer = entry_dict["Referer"]
        self.user_agent = entry_dict["Useragent"]

        # clfparser handles dates in a weird way (ignoring timezones)
        self.time = datetime.strptime(entry_dict['t'][1:-1], '%d/%b/%Y:%H:%M:%S %z').astimezone(timezone.utc)

    @staticmethod
    def _is_valid(entry_dict: Dict[str, str]) -> bool:
        """ Checks if the input is valid

        The reason for this check is that clfparser has no visible error reporting,
        instead it just fills all the fields to ""
        :param entry_dict: dict representing the entry, as given by CLFParser.logDict
        :return: True if the entry is valid
        """
        for v in entry_dict.values():
            if v:
                return True
        return False

    def __eq__(self, other):
        """
        Tests for equality between self and an other instance

        This is mostly used for unit tests

        :param other: other instance
        :return: is equal
        """
        if not isinstance(other, LogEntry):
            return False
        return self.__dict__ == other.__dict__
