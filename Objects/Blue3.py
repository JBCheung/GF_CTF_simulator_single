from GameFrame import BlueBot, Globals
from Objects.global_functions import Global_Functions_Blue
from enum import Enum

class state(Enum):
    WAIT=1
    ATTACK=2
    DEFEND=3
    RETURN=4

class Blue3(Global_Functions_Blue, BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.state=state.ATTACK
        

    def tick(self):
        """
        Attack bot - around the flag
        """
        halfway = Globals.SCREEN_WIDTH/2
        flag = Globals.blue_flag
        dist, enemy = self.closest_enemy_to_flag()
        #determine state
        if (enemy.x < halfway > self.x) and dist<250 and self.points_toward_coordinate(enemy.x, enemy.y, error=120):
            self.state = state.DEFEND
        elif self.has_flag == False:
            self.state = state.ATTACK   
        elif self.has_flag:
            self.state = state.RETURN
        # execute actions for each state
        if self.state == state.ATTACK:
            # on friendly side
            if self.x < halfway:
                # if closest enemy in front of self, 150 pixels away, and on friendly side
                dist, enemy = self.closest_enemy()
                if self.is_infront(enemy, dist=150) and enemy.x<halfway:
                    self.turn_towards(enemy.x, enemy.y)
                else:
                    self.turn_towards(halfway, Globals.SCREEN_HEIGHT/10 ,speed=Globals.FAST)
                self.drive_forward(speed=Globals.FAST)
            elif self.x <= flag.x:
                # if past halfway and before reaching point, drive forwards 
                self.turn_towards(Globals.SCREEN_WIDTH, self.y, speed=Globals.FAST)
                self.drive_forward(speed=Globals.FAST)
            else:
                # reached point, then drive towards flag, while dodging enemies
                self.swerve_turn_towards(flag.x,flag.y)
                self.drive_forward(speed=Globals.FAST)
        elif self.state == state.RETURN:
            # return flag home, while dodging enemies
            self.swerve_turn_towards(0, self.y)
            self.drive_forward(speed=Globals.FAST)
        elif self.state == state.DEFEND:
            self.turn_towards(enemy.x, enemy.y, speed=Globals.FAST)
            self.drive_forward(speed=Globals.FAST)
        
        
        
        
        '''
        halfway = Globals.SCREEN_WIDTH/2
        flag = Globals.blue_flag
        if self.has_flag == False:
            if self.x < halfway:
                self.turn_towards(halfway, Globals.SCREEN_HEIGHT*3/4 ,speed=Globals.FAST)
                self.drive_forward(speed=Globals.FAST)
            else:
                # if enemy in radius, then turn away from enemy
                self.turn_towards(flag.x,flag.y,speed=Globals.FAST)
                self.drive_forward(speed=Globals.FAST)
        else:
            self.turn_towards(0, self.y)
            self.drive_forward(speed=Globals.FAST)
        '''

