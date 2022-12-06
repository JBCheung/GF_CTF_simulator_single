import os
import pygame
from GameFrame.Globals import Globals, Simulation_Flags
import time

class Level:

    def __init__(self):
        self.objects = []
        self.running = False
        self.quitting = False
        self.user_events = []
        self.flags = set()

    def run(self):
        self.running = True
        for obj in self.objects:
            self.init_collision_list(obj)
        
        while self.running:
            self.tick()
            for obj in self.objects:
                obj.prev_x = obj.x
                obj.prev_y = obj.y

            # - Process user events - #
            self.process_user_events()
            # Check collisions
            for item in self.objects:
                item.check_collisions()
            # Call Update on all objects
            for item in self.objects:
                item.update()
                item.step()
        return self.flags
    
    def add_room_object(self, room_object):
        # - Add to room objects list - #
        if len(self.objects) == 0:
            self.objects.append(room_object)
        else:
            for index, item in enumerate(self.objects):
                if item.depth >= room_object.depth:
                    self.objects.insert(index, room_object)
                    break
                elif index == len(self.objects) - 1:
                    self.objects.append(room_object)
                    break
                
        if self.running:
            for obj in self.objects:
                self.init_collision_list(obj)

    def load_image(self, file_name):
        return os.path.join('Images', file_name)

    def init_collision_list(self, room_object):
        # - Initialise collision list for object - #
        for obj_name in room_object.collision_object_types:
            for obj_instance in self.objects:
                if type(obj_instance).__name__ == obj_name and obj_instance is not room_object:
                    room_object.collision_objects.append(obj_instance)

    def catch_events(self, events):
        pass

    def delete_object(self, obj):
        for index, list_obj in enumerate(self.objects):
            if list_obj is obj:
                self.objects.pop(index)
            else:
                list_obj.remove_object(obj)
        # Remove any timed function calls for the deleted object
        for index, event_method in enumerate(self.user_events):
            obj_inst = event_method[1].__self__
            if obj_inst is obj:
                self.user_events.pop(index)

    def set_timer(self, ticks, function_call):
        self.user_events.append([ticks, function_call])

    def process_user_events(self):
        for index, user_event in enumerate(self.user_events):
            user_event[0] -= 1
            if user_event[0] <= 0:
                user_event[1]()
                self.user_events.pop(index)

    def tick(self):
        pass
