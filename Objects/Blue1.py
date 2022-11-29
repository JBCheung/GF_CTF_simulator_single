from GameFrame import BlueBot, Globals
from Objects.global_functions import Global_Functions_Blue
from enum import Enum
import os
import random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

class state(Enum):
    WAIT = 1
    ATTACK = 2
    JAIL_BREAK = 3
    RETURN = 4
    TURN = 5
    DEFEND=6


class Blue1(Global_Functions_Blue, BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.state = state.ATTACK
        self.rand_crossing_pointY = random.randint(Globals.SCREEN_HEIGHT/2, Globals.SCREEN_HEIGHT-50)
        self.initial_wait = random.randint(0, 5)
        self.wait_count = 0
        self.DISTRACTION = False
        
    
    def tick(self):       
        """distraction or random attacker"""
        if self.DISTRACTION:
            self.distraction_bot()
        else:
            self.random_attacker()

    
    
    def distraction_bot(self):
        """
        distraction bot
        """
        flag = Globals.blue_flag
        dist, closest = self.closest_enemy()
        print(dist)
        if self.wait_count < self.initial_wait:
            self.wait_count += 1
        else:
            if self.has_flag:
                self.turn_towards(0, self.y)
                self.drive_forward(Globals.FAST)
            else:
                if dist<=150:
                    print('yes')
                    infront=self.is_infront(closest,dist=150)
                    left=self.is_left(closest.x,closest.y)
                    speed=Globals.FAST if dist<90 else Globals.MEDIUM
                    if infront ==True and left== True:
                        self.turn_right(speed)
                        self.drive_forward(Globals.FAST)
                        print("left")
                    elif infront == True and left== False:
                        self.turn_left(speed)
                        self.drive_forward(Globals.FAST)
                        print("right")
                    else:
                        self.drive_forward(Globals.FAST)
                        print("chase")

                else:
                    if self.x<=Globals.SCREEN_WIDTH/2:
                        self.turn_towards(700,random.randint(1,360))
                        self.drive_forward(Globals.FAST)
                    else:
                        self.turn_towards(flag.x,flag.y,Globals.FAST)
                        self.drive_forward(Globals.FAST)
    
    
    
    def random_attacker(self):
        '''attacker bot - random crossing'''       
        # declare variables required 
        halfway = Globals.SCREEN_WIDTH/2
        flag = Globals.blue_flag
        flagx, flagy = flag.rect.center
        dist, enemy = self.closest_enemy_to_flag()
        camping_dist, camping_enemy = self.closest_bot_to_coord(Globals.red_bots,x=flagx,y=flagy)
        enemy_camping = True if camping_dist <= 30 else False
        # determine state
        if enemy.x<halfway and self.x<halfway:
            self.state = state.DEFEND
        if self.has_flag == False:
            self.state = state.ATTACK   
        elif self.has_flag:
            self.state = state.RETURN
        # execute action based on current state
        if self.state == state.ATTACK:
            # if self on friendly side
            if not self.is_past_halfway(self):
                # if enemy on friendly side and enemy is infront of self, attack enemy
                if self.is_infront(enemy, dist=150) and self.is_past_halfway(enemy):
                    self.turn_towards(enemy.x, enemy.y)
                else:
                    self.turn_towards(halfway, self.rand_crossing_pointY ,speed=Globals.FAST)
                self.drive_forward(speed=Globals.FAST)
            else:
                # while not driving towards random point, randomise point
                self.rand_crossing_pointY = random.randint(50, Globals.SCREEN_HEIGHT-50)
                # swerve around incoming enemies, and drive forward unless about to collide with camper bot
                self.swerve_turn_towards(flag.x, flag.y)
                if not (enemy_camping and self.point_to_point_distance(self.x, self.y, flag.x, flag.y)<50):
                    self.drive_forward(speed=Globals.FAST) 
        elif self.state == state.RETURN:
            self.turn_towards(0, self.y)
            self.drive_forward(speed=Globals.FAST)
        elif self.state == state.DEFEND:
            self.turn_towards(enemy.x, enemy.y, speed=Globals.FAST)
            self.drive_forward(speed=Globals.FAST)
    
            
    '''
        flag = Globals.red_flag
        home = flag.rect.center
        x = self.rect.centerx
        y = self.rect.centery
        RADIUS = 100
        DEBUG = True
        error = 5
        FLAG_RADIUS = 10
        if not self.point_to_point_distance(self.x,self.y,flag.x,flag.y) < 5:
            target_angle = self.get_rotation_to_coordinate(x,y)
            target_angle = 360+target_angle if target_angle<0 else target_angle
            rotation_to_coord = int(self.get_rotation_to_coordinate(flag.x,flag.y)-self.curr_rotation)%360
            print(f"{rotation_to_coord=}")
            if int(rotation_to_coord) == 0:                                      #abs(int(rotation_to_coord)) < 4 or abs(int(rotation_to_coord)) > 356:
                self.drive_forward(speed=Globals.FAST)
            else:
                self.clean_turn_towards(flag.x, flag.y)'''
            
            
    

          

