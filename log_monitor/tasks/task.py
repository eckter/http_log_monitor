import time


class Task:
    def __init__(self, interval):
        self.interval = interval
        self.next_timer = time.time() + interval

    def update(self):
        if time.time() > self.next_timer:
            self.next_timer += self.interval
            self._on_timer()

    def _on_timer(self):
        pass

    def register_entry(self, entry):
        pass
