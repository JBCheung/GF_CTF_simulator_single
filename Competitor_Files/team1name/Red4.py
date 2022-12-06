from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 1
    ATTACK = 2


class Red4(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)

        self.curr_state = STATE.WAIT

    def tick(self):

       pass
