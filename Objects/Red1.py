import time
from GameFrame import RedBot, Globals
from Objects.global_functions import Global_Functions_Red
import random, math
from enum import Enum

class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    JAIL_BREAK = 3
    AI = 4

class Red1(Global_Functions_Red, RedBot):
    # X, Y of 1280 x 720
    # halved   640 x 360
    # Blue  <  640 x 360
    # Red   >  640 x 360
    # 160 x 90 blocks


    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(300,700)
        sh = Globals.SCREEN_HEIGHT / 4
        self.grids = [
                (80, sh/2), (240, sh/2+sh), (400, (sh/2)+(sh*2)), (560, (sh/2)+(sh*3)),
                (80, (sh/2)+(sh*1)), (240, (sh/2)+(sh*1)), (400, (sh/2)+(sh*1)), (560, (sh/2)+(sh*1)),
                (80, (sh/2)+(sh*2)), (240, (sh/2)+(sh*2)), (400, (sh/2)+(sh*2)), (560, (sh/2)+(sh*2)),
                (80, (sh/2)+(sh*3)), (240, (sh/2)+(sh*3)), (400, (sh/2)+(sh*3)), (560, (sh/2)+(sh*3))
                ]    
        
    def tick(self):
        # start =time.perf_counter_ns()
        # for n in range(45):
        #     self.rotate(1)
        # end = time.perf_counter_ns()
        # print(f"{end-start}")
        
        # print(f"{self.rect.width} {self.rect.height}")
        #other_rect = 
        #print(f'{self.rect.collidepoint}')
        
        
        if self.has_flag:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.in_blue_territory():
            dist, closest = self.closest_enemy()
            if self.enemy_close_to_flag() < 10:
                self.drive_towards_random()
            else:
                self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
                self.drive_forward(Globals.FAST)
        else:
            self.drive_towards_random()
    
    def drive_towards_random(self):
        target_loc = self.grids[random.randint(11, 12)]
        self.turn_towards(target_loc[0], target_loc[1], Globals.FAST)
        self.drive_forward(Globals.FAST)

    def enemy_close_to_flag(self):
        dist, closest = self.closest_enemy()
        p1 = [x, y] = closest.get_position()
        p2 = [ Globals.red_flag.x, Globals.red_flag.y ]
        distance = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
        # print(distance)
        return distance

    def in_blue_territory(self):
        w = Globals.SCREEN_WIDTH / 2
        x, y = self.get_position()
        if x < w:
            return True

        return False