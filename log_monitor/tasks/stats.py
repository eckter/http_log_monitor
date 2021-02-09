from .task import Task


class Stats(Task):
    def __init__(self, configs):
        super().__init__(configs["delay"])

    def _on_timer(self):
        print("yay timer!")