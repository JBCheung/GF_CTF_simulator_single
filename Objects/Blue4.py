from GameFrame import BlueBot, Globals
from Objects.global_functions import Global_Functions_Blue
import random
DEBUG = False


class Blue4(Global_Functions_Blue, BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.tick_no = 0
        self.DEBUG = DEBUG
        
        
    def tick(self):
        """camper bot"""
        flag = Globals.red_flag
        selfx, selfy = self.rect.center
        flagx, flagy = flag.rect.center
        dist, closest = self.closest_enemy()
        # if center of self not on flag, then 
        if self.point_to_point_distance(selfx,selfy,flagx,flagy) > 0:
            rotation_to_coord = abs(self.relative_rotation_to_coordinate(flagx,flagy))
            if DEBUG: print(f"in tick: {rotation_to_coord=}")
            if int(rotation_to_coord) == 0:
                self.clean_drive_forward2(flagx, flagy)
            else:
                self.clean_turn_towards(flagx, flagy)
        else:
            self.turn_towards(closest.x, closest.y, speed=Globals.FAST)

        self.tick_no += 1
        
    
        
    '''
    def tick(self):
        """camper bot"""
        flag = Globals.red_flag
        selfx, selfy = self.rect.center
        flagx, flagy = flag.rect.center
        dist, closest = self.closest_enemy()
        enemies_have_flag = False
        for enemy in Globals.red_bots:
            if enemy.has_flag:
                enemies_have_flag = True
                break
        # if
        if self.point_to_point_distance(selfx,selfy,flagx,flagy) > 0:
            rotation_to_coord = abs(self.relative_rotation_to_coordinate(flagx,flagy))
            if DEBUG: print(f"in tick: {rotation_to_coord=}")
            if int(rotation_to_coord) == 0 or enemies_have_flag:
                self.clean_drive_forward2(flagx, flagy)
            else:
                self.clean_turn_towards(flagx, flagy)
        else:
            self.turn_towards(closest.x, closest.y, speed=Globals.FAST)

        self.tick_no += 1
    '''
    
    
    
    def clean_drive_forward2(self, x, y):
        '''
        x, y should be coordinate that your driving towards 
        '''
        selfx, selfy = self.rect.center
        distance = self.point_to_point_distance(selfx, selfy, x, y)
        
        if distance >= Globals.FAST:
            self.drive_forward(speed=Globals.FAST)
            if DEBUG: print('MOVE Fast')
        elif distance >= Globals.MEDIUM:
            self.drive_forward(speed=Globals.MEDIUM)
            if DEBUG: print('MOVE Medium')      
        elif distance >= Globals.SLOW:
            self.drive_forward(speed=Globals.SLOW)
            if DEBUG: print('MOVE Slow') 
        else:
            self.move_in_direction(self.curr_rotation, distance)  
            if DEBUG: print(f"this distance should be less than 3, otherwise cheating {distance}")  
          
            
    def points_toward_coordinate(self,x,y,error=10) -> bool:
        target_angle = self.centred_get_rotation_to_coordinate(x,y)
        target_angle = 360+target_angle if target_angle<0 else target_angle
        return (self.curr_rotation > target_angle-error) and (self.curr_rotation < target_angle+error)
    
    def closest_enemy(self):
        enemy_list = Globals.red_bots
        closest = enemy_list[0]
        dist = self.point_to_point_distance(self.x, self.y, closest.x, closest.y)
        for enemy in enemy_list:
            temp_dist = self.point_to_point_distance(self.x, self.y, enemy.x, enemy.y)
            if temp_dist < dist:
                closest = enemy
                dist = temp_dist
        return dist, closest