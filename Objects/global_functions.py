from GameFrame import BlueBot, RedBot, Bot, Globals


class Global_Functions(Bot):
    DEBUG=False
    
    def closest_bot_to_coord(self, group_of_bots:list, x:float, y:float, other_condition=lambda bot: True) -> tuple[float, Bot]:
        closest = group_of_bots[0]
        closestx, closesty = closest.rect.center
        dist = self.point_to_point_distance(x,y,closestx, closesty)
        for bot in group_of_bots:
            if not other_condition(bot):
                continue
            botx, boty = bot.rect.center
            temp_dist = self.point_to_point_distance(x,y,botx,boty)
            if temp_dist < dist:
                closest = bot
                dist = temp_dist
        return dist, closest
   
    
    
    def bad_clean_turn_towards(self, x, y):
        '''
        x, y should be flag coords
        '''
        rotation_to_coord = (self.centred_get_rotation_to_coordinate(x,y)-self.curr_rotation)%360
        if self.DEBUG: print(f"in clean_turn_towards: {rotation_to_coord=}")
        
        if abs(rotation_to_coord) >= Globals.FAST or abs(rotation_to_coord-360) <= Globals.FAST:
            self.turn_towards(x, y, speed=Globals.FAST)
            if self.DEBUG: print('turn Fast')
        elif abs(rotation_to_coord) >= Globals.MEDIUM or abs(rotation_to_coord-360) <= Globals.MEDIUM:
            self.turn_towards(x, y, speed=Globals.MEDIUM)
            if self.DEBUG: print('turn Medium')
        elif abs(rotation_to_coord) >= Globals.SLOW or abs(rotation_to_coord-360) <= Globals.SLOW:
            self.turn_towards(x, y, speed=Globals.SLOW)
            if self.DEBUG: print('turn Slow')
        elif abs(rotation_to_coord) < Globals.SLOW or abs(rotation_to_coord-360) > Globals.SLOW:
            self.rotate(rotation_to_coord)
            if self.DEBUG: print(f"this angle should be less than 3, otherwise cheating {rotation_to_coord}")
        return
    def clean_turn_towards(self, x, y):    
        target_angle = self.centred_get_rotation_to_coordinate(x,y)
        rotation_to_coord = (target_angle-self.curr_rotation)%360
        
        if rotation_to_coord > 180:
            rotation_to_coord -= 360
        if self.DEBUG: print(f"clean_turn_towards: {rotation_to_coord=} {target_angle=} {self.curr_rotation=}")
                
        FAST = 9
        MEDIUM = 6
        SLOW = 3
        if abs(rotation_to_coord) >= FAST: 
            self.turn_towards(x, y, speed=Globals.FAST)
            if self.DEBUG: print('turn Fast')
        elif abs(rotation_to_coord) >= MEDIUM: 
            self.turn_towards(x, y, speed=Globals.MEDIUM)
            if self.DEBUG: print('turn Medium')
        elif abs(rotation_to_coord) >= SLOW: 
            self.turn_towards(x, y, speed=Globals.SLOW)
            if self.DEBUG: print('turn Slow')
        elif abs(rotation_to_coord) < SLOW:
            self.rotate(rotation_to_coord)
            if self.DEBUG: print(f"turn CUSTOM: {rotation_to_coord}")
        return
    
    def clean_drive_forward(self, x, y):
        '''
        x, y should be coordinate that your driving towards 
        '''
        selfx, selfy = self.rect.center
        distance = self.point_to_point_distance(selfx, selfy, x, y)
        if self.DEBUG: print(f'in clean_drive_forwards: {distance=}')
        if self.DEBUG: print(f"{self.x=} {self.y=}")
        
        
        if distance >= Globals.FAST:
            self.drive_forward(speed=Globals.FAST)
            if self.DEBUG: print('MOVE Fast')
        elif distance >= Globals.MEDIUM:
            self.drive_forward(speed=Globals.MEDIUM)
            if self.DEBUG: print('MOVE Medium')      
        elif distance >= Globals.SLOW:
            self.drive_forward(speed=Globals.SLOW)
            if self.DEBUG: print('MOVE Slow') 
        elif distance < Globals.SLOW:
            self.move_in_direction(self.curr_rotation, distance)  
            if self.DEBUG: print(f"this distance should be less than 3, otherwise cheating {distance}") 
        else:
            print('something is REALLY BAD in clean_drive_forwards')
            raise ValueError('in method: clean_drive_forwards() - negative length input')
        return
    def is_infront(self, enemy, dist=100):
        '''
        tests if given enemy is a distance infront of self
        '''
        #selfx, selfy = self.rect.center
        enemyx, enemyy = enemy.rect.center
        if self.point_to_point_distance(self.x, self.y, enemyx, enemyy) <= dist:
            # similar to is pointing towards with large error 
            return self.points_toward_coordinate(enemyx, enemyy, error=120)      
    def points_toward_coordinate(self,x,y,error=10) -> bool:
        target_angle = self.centred_get_rotation_to_coordinate(x,y)
        target_angle = 360+target_angle if target_angle<0 else target_angle
        return (int(self.curr_rotation) >= int(target_angle-error)) and (int(self.curr_rotation) <= int(target_angle+error))

    def quadrant(self, x, y):
        '''
        which quadrant coordinate is from self
        
        returns  is_left, is_right, is_backleft, is_backright
        '''
        X1,X2,Y1,Y2=self.x,x,self.y,y
        XD,YD=X1-X2 if X1>X2 else X2-X1,Y1-Y2 if Y1>Y2 else Y2-Y1
        # print(X1,X2,Y1,Y2)

        QUAD1=False
        QUAD2=False
        QUAD3=False
        QUAD4=False
        
        if X1<X2 and Y1>Y2:
            #print("""Quad 1""")
            QUAD1=True
            #print("drive")

        elif X1>X2 and Y1>Y2:
            # print("""Quad 2""")
            QUAD2=True
            #    print("drive")
                
        elif X1>X2 and Y1<Y2:
            #   print("""Quad 3""")
            QUAD3=True
            #    print("drive")

        elif X1<X2 and Y1<Y2:
            #  print("""Quad 4""")
            QUAD4=True
        
        return (QUAD4,QUAD1,QUAD3,QUAD2)

    def is_left(self,x,y):
        target_angle = self.get_rotation_to_coordinate(x,y)
        target_angle = 360+target_angle if target_angle<0 else target_angle
        selfangle = 360 +self.angle if self.angle<0 else self.angle 
        if target_angle<=selfangle<=target_angle+180 or target_angle+360<=selfangle<=target_angle+540 :
            return(False)
        else:
            return(True)

    def ticks_to(self, x, y):
        # dummy_bot = super().__init__(self.room, self.x, self.y)
        # ticks = 0
        # while dummy_bot       
        
        rotation_to_coord = abs(self.relative_rotation_to_coordinate(x, y))
        distance = self.point_to_point_distance(self.x, self.y, x, y)
        ticks=0
        ticks += rotation_to_coord//Globals.FAST
        rotation_to_coord %= Globals.FAST
        ticks += rotation_to_coord//Globals.MEDIUM
        rotation_to_coord %= Globals.MEDIUM
        ticks += rotation_to_coord//Globals.SLOW
        rotation_to_coord %= Globals.SLOW
        if 0 < rotation_to_coord < Globals.SLOW:
            ticks += 1
            
        ticks += distance//Globals.FAST
        distance %= Globals.FAST
        ticks += distance//Globals.MEDIUM
        distance %= Globals.MEDIUM
        ticks += distance//Globals.SLOW
        distance %= Globals.SLOW
        if 0 < distance < Globals.SLOW:
            ticks += 1
        
        return ticks

    def relative_rotation_to_coordinate(self, x, y):
        '''
        returns angle to ccoordinate normalised to self's north. if coordinate directly behind self, return 180 (not -180)
        '''
        rotation_to_coord = (self.centred_get_rotation_to_coordinate(x,y)-self.curr_rotation)%360
        if rotation_to_coord > 180:
            rotation_to_coord -= 360
        return rotation_to_coord
    
    def centred_get_rotation_to_coordinate(self, x, y):
        import math
        distance_x = self.rect.centerx - x
        distance_y = self.rect.centery - y
        return math.degrees(math.atan2(distance_x, distance_y))
    
    def weighted_least_dist(self, enemy_team, coords_along_border=4, exponent=-1, max_distance=400, min_dist_to_flag=25):
        '''min distance allows for bots past a certain range to be excluded, useful for outlying the jailer bot or camper bot'''
        import math
        # declare variables and containers for data.
        if coords_along_border >= Globals.SCREEN_HEIGHT:
            coordinates=[(Globals.SCREEN_WIDTH/2, y) for y in range(50, Globals.SCREEN_HEIGHT-50)]
        else: 
            coordinates=[(Globals.SCREEN_WIDTH/2, Globals.SCREEN_HEIGHT*i/coords_along_border+1) for i in range(1, coords_along_border)]
        values = []
        # boolean for which team the enemy_team is
        is_red = isinstance(enemy_team[0], RedBot)
        flag = Globals.blue_flag if is_red else Globals.red_flag
        # calculate weight for each coordinate 
        for coord in coordinates:
            curr_value = 0
            # loop through enemies, check requirements based on max_distance and min_dist_to_flag
            for enemy in enemy_team:
                distance = self.point_to_point_distance(coord[0], coord[1], enemy.x, enemy.y)
                dist_to_flag = self.point_to_point_distance(enemy.x, enemy.y, flag.x, flag.y)
                if (0 < distance < max_distance) and (dist_to_flag > min_dist_to_flag) and (not self.is_past_halfway(enemy)):
                    # if past tests, add value to weight, larger values weighted less, (better for the test)
                    curr_value += distance**exponent
            # the min() function should prioritise the value, then the overall distance to travel to get to the flag
            dist_to_flag_plus_self = self.point_to_point_distance(coord[0], coord[1], flag.x, flag.y) + self.point_to_point_distance(coord[0], coord[1], self.x, self.y)
            values.append((curr_value,dist_to_flag_plus_self , coord))
        # find coordinate with least weight, then least distance to travel to the flag, then return coord. 
        value, coord_dist_to_flag_plus_self, coord = min(values)
        if self.DEBUG: print(f'in {self}: {value=} {coord=}')
        return coord
        
        
            
    def is_past_halfway(self, bot):
        halfway = Globals.SCREEN_WIDTH/2
        if isinstance(bot, RedBot):
            # then, bot is a red bot, and home is right side
            return bot.x < halfway
        elif isinstance(bot, BlueBot):
            return bot.x > halfway
                 
        

class Global_Functions_Blue(Global_Functions, BlueBot):
    DEBUG=False
        
    def closest_enemy(self, other_condition=lambda enemy: True):
        """other condition function is passed the enemy and returns false if the enemy should be excluded entirely from being the next closest (overrides judging solely by distance)
        implemented so that functions like closest enemy that on enemy side can be more easily implemented
        """
        selfx, selfy = self.rect.center
        return self.closest_bot_to_coord(
            group_of_bots=Globals.red_bots,
            x=selfx,
            y=selfy,
            other_condition=other_condition
            )
    
    def closest_enemy_on_enemyside(self):
        return self.closest_enemy(other_condition=lambda enemy: not self.is_past_halfway(enemy))
    
    def closest_enemy_to_flag(self):
        flagx, flagy = Globals.red_flag.rect.center
        return self.closest_bot_to_coord(
            group_of_bots=Globals.red_bots,
            x=flagx,
            y=flagy,
        )        
        
    def swerve_turn_towards(self, x, y):
        dist, enemy = self.closest_enemy()
        if self.is_infront(enemy, dist=200):
            # isleft, isright, isbackleft, isbackright = self.quadrant()
            if self.y<100:
                self.turn_right(speed=Globals.FAST)
            elif self.y>Globals.SCREEN_HEIGHT-100:
                self.turn_left(speed=Globals.FAST)
            elif self.x>x:
                self.turn_towards(x, y, speed=Globals.FAST)
            else:
                rotation_to_coord = int(self.centred_get_rotation_to_coordinate(enemy.x,enemy.y)-self.curr_rotation)%360
                if rotation_to_coord < 180: # less than 180 degree clockwise rotation to enemy
                    self.turn_right(speed=Globals.FAST)
                elif rotation_to_coord > 180: # less than 180 degree anticlockwise rotation to enemy
                    self.turn_left(speed=Globals.FAST)
        else:
            self.turn_towards(x,y,speed=Globals.FAST)



class Global_Functions_Red(Global_Functions, RedBot):
    DEBUG=False
    
    def closest_enemy(self, other_condition=lambda enemy: True):
        """other condition function is passed the enemy and returns false if the enemy should be excluded entirely from being the next closest (overrides judging solely by distance)
        implemented so that functions like closest enemy that on enemy side can be more easily implemented
        """
        selfx, selfy = self.rect.center
        return self.closest_bot_to_coord(
            group_of_bots=Globals.blue_bots,
            x=selfx,
            y=selfy,
            other_condition=other_condition
            )
    
    def closest_enemy_to_flag(self):
        flagx, flagy = Globals.blue_flag.rect.center
        return self.closest_bot_to_coord(
            group_of_bots=Globals.blue_bots,
            x=flagx,
            y=flagy,
        ) 
              
    def swerve_turn_towards(self, x, y):
        dist, enemy = self.closest_enemy()
        if self.is_infront(enemy, dist=200):
            # isleft, isright, isbackleft, isbackright = self.quadrant()
            if self.y<100:
                self.turn_left(speed=Globals.FAST)
            elif self.y>Globals.SCREEN_HEIGHT-100:
                self.turn_right(speed=Globals.FAST)
            elif self.x<x:
                self.turn_towards(x, y, speed=Globals.FAST)
            else:
                rotation_to_coord = int(self.centred_get_rotation_to_coordinate(enemy.x,enemy.y)-self.curr_rotation)%360
                if rotation_to_coord < 180: # less than 180 degree clockwise rotation to enemy
                    self.turn_right(speed=Globals.FAST)
                elif rotation_to_coord > 180: # less than 180 degree anticlockwise rotation to enemy
                    self.turn_left(speed=Globals.FAST)
        else:
            self.turn_towards(x,y,speed=Globals.FAST)