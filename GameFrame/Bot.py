from GameFrame import RoomObject
from GameFrame import Globals, Simulation_Flags
import pygame

class Bot(RoomObject):
    def __init__(self, room, x, y,size=60, font='Comic Sans MS', colour=(0, 0, 0), bold=False):
        RoomObject.__init__(self, room, x, y)
        self.starting_x = x
        self.starting_y = y
        self.has_flag = False
        self.jailed = False
        self.prev_distance_moved = 0
        self.distance_moved = 0
        
        # for statistics 
        self.points=0
        self.deaths=0
        self.kills=0
        self.time_with_flag=0
        self.friends_released=0

        self.if_cheating_flag = None


    def step(self):
        if not self.jailed:
            self.prev_distance_moved = self.distance_moved
            self.frame()
            if self.x <= 0:
                self.blocked()
            elif self.x >= Globals.SCREEN_WIDTH - self.width:
                self.blocked()

            if self.y <= 0:
                self.blocked()
            elif self.y >= Globals.SCREEN_HEIGHT - self.height:
                self.blocked()

    def frame(self):
        pass

    def turn_left(self, speed=Globals.SLOW):
        if self.has_flag:
            self.rotate(40)
        elif speed == Globals.FAST:
            self.rotate(9)
        elif speed == Globals.MEDIUM:
            self.rotate(6)
        else:
            self.rotate(3)

    def turn_right(self, speed=Globals.SLOW):
        if self.has_flag:
            self.rotate(-40)
        elif speed == Globals.FAST:
            self.rotate(-9)
        elif speed == Globals.MEDIUM:
            self.rotate(-6)
        else:
            self.rotate(-3)

    def turn_towards(self, x, y, speed=Globals.SLOW):

        target_angle = int(self.get_rotation_to_coordinate(x, y))

        if target_angle < 0:
            target_angle = 360 + target_angle

        if self.curr_rotation <= 180:
            if self.curr_rotation + 2 < target_angle < self.curr_rotation + 180:
                self.turn_left(speed)
            else:
                self.turn_right(speed)
        else:
            if self.curr_rotation + 2 < target_angle < 360 or 0 <= target_angle < self.curr_rotation - 180:
                self.turn_left(speed)
            else:
                self.turn_right(speed)

    def drive_forward(self, speed=Globals.SLOW):
        if speed == Globals.FAST:
            self.move_in_direction(self.curr_rotation, Globals.FAST)
        elif speed == Globals.MEDIUM:
            self.move_in_direction(self.curr_rotation, Globals.MEDIUM)
        else:
            self.move_in_direction(self.curr_rotation, Globals.SLOW)

    def drive_backward(self):
        direction = self.curr_rotation - 180
        if direction < 0:
            direction = 360 + direction
        self.move_in_direction(direction, Globals.SLOW)

    def rotate(self, angle):
        if abs(angle) > 9:
            if not (abs(angle) <= 40 and self.has_flag) and self.curr_rotation!=0:
                self.room.flags.add(self.if_cheating_flag)
                self.room.flags.add(f'{self.__class__.__name__} turning too fast ({angle=})')
        return super().rotate(angle)
    
    def move_in_direction(self, angle, distance):
        self.distance_moved += distance
        # find difference in distance moved from last tick to currently. 
        # rounding to account for the imprecisions of floating point arithmetic
        if round(abs(self.distance_moved-self.prev_distance_moved), 10) > Globals.FAST:
            self.room.flags.add(self.if_cheating_flag)
            # if a cheating flag message for this bot isn't already in the flags set
            if True not in [str(flag).startswith(self.__class__.__name__) for flag in self.room.flags]:
                self.room.flags.add(f'{self.__class__.__name__} moving too fast ({distance=}) ({self.distance_moved-self.prev_distance_moved})')
        return super().move_in_direction(angle, distance)
        #dist = self.point_to_point_distance(self.prev_x, self.prev_y, self.x, self.y)
