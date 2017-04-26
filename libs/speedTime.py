import time


class SpeedTime:
    """
    test db query or code speed time
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def end(self, text="time spend"):
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time

        print("{}={}".format(text, elapsed))
