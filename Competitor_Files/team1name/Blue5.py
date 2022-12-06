from GameFrame import BlueBot, Globals
import random


class Blue5(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(30, 90)
        self.wait_count = 0

    def tick(self):
        pass
