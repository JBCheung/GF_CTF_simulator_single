from GameFrame import BlueBot, Globals
from GameFrame.RedBot import RedBot
from Objects.global_functions import Global_Functions_Blue
from enum import Enum
import random
import pygame

class state(Enum):
    INIT=1
    RETURN=2
    WAIT=3
    JAILBREAK=4


class Blue5(Global_Functions_Blue, BlueBot):
    
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.state = state.INIT
        
        
    def tick(self):
        """Pure Jail Bot"""
        WAVES = False 
        if not WAVES:
            self.turn_towards(0,0)
            self.drive_forward(speed=Globals.FAST)
        else:
            NUM_ATTACKING_BOTS = 3
            '''moving bot to location in INIT states'''
            jailed_bot_rect = pygame.rect.Rect(20,20,self.width,self.height)
            if self.state == state.INIT:
                self.clean_turn_towards(20,20)
                self.clean_drive_forward(20,20)
                if self.rect.colliderect(jailed_bot_rect):
                    self.state = state.RETURN
            elif self.state == state.RETURN:
                self.drive_backward()
                if not self.rect.colliderect(jailed_bot_rect):
                    self.state = state.WAIT
            elif self.state == state.WAIT:
                current_jailed = 0
                for friend in Globals.blue_bots:
                    if friend.jailed:
                        current_jailed+=1
                if current_jailed >= NUM_ATTACKING_BOTS:
                    self.drive_forward()
                    self.state = state.JAILBREAK
            elif self.state==state.JAILBREAK:
                current_jailed = 0
                for friend in Globals.blue_bots:
                    if friend.jailed:
                        current_jailed+=1
                if current_jailed > 0:
                    self.drive_forward()
                else:
                    self.state = state.RETURN
                
        
        
