from GameFrame import BlueBot, Globals
from Objects.global_functions import Global_Functions_Blue
from enum import Enum


class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    RETURN = 3
    ATTACK_TO_POINT =4


class Blue2(Global_Functions_Blue, BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.halfway_point_Y = Globals.SCREEN_HEIGHT/4
        self.tick_no = 0
        
        
    def tick(self):
        """attack bot - best border point"""   
        # declare variables
        halfway = Globals.SCREEN_WIDTH/2
        halfway_Y = Globals.SCREEN_HEIGHT/2
        flag = Globals.blue_flag
        dist, enemy = self.closest_enemy()
        if self.has_flag == False:
            # if not close to border, find best point to cross at
            if self.x < halfway-80:
                # if self.x < halfway/2:
                self.halfway_point_Y = self.weighted_least_dist(Globals.red_bots, coords_along_border=Globals.SCREEN_HEIGHT)[1]
                #small defence manuvour to catch any close enemies
                if self.is_infront(enemy, dist=150) and enemy.x<halfway:
                    self.turn_towards(enemy.x, enemy.y)
                else:
                    self.turn_towards(halfway, self.halfway_point_Y,speed=Globals.FAST)
                self.drive_forward(speed=Globals.FAST)
            else:
                # if enemy in radius, then turn away from enemy
                self.swerve_turn_towards(flag.x, flag.y)
                self.drive_forward(speed=Globals.FAST)
        else:
            # if has flag, return back to home
            self.swerve_turn_towards(0, self.y)
            self.drive_forward(speed=Globals.FAST)
        self.tick_no += 1