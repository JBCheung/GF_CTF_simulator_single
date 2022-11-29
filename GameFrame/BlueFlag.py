from GameFrame import RoomObject, Globals


class BlueFlag(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        self.set_rect(32, 32)

    def step(self):
        if self.x < Globals.SCREEN_WIDTH/2:
            Globals.winner = 'Blue'
            self.room.running = False
