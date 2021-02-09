class LogEntry:
    """
    Represents the content of an entry following Common Log Format
    """
    def __init__(self, string_entry):
        self.host, \
            self.identity, \
            self.user_id, \
            self.time, \
            self.request, \
            self.status, \
            self.size = string_entry.split()

        self.request = self.request[1:-1]   # removes quotes
