import math
import os
import pygame
from GameFrame.Globals import Globals
import time

class RoomObject:

    def __init__(self, room, x, y):
        self.room = room
        self.depth = 0
        self.x = x
        self.y = y
        self.rect = 0
        self.prev_x = x
        self.prev_y = y
        self.width = 0
        self.height = 0
        self.curr_rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0
        self.angle = 0

        self.collision_object_types = set()
        self.collision_objects = []

    def set_rect(self, width, height):
        'no longer sets any image. only creates the objects rectangle'
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def register_collision_object(self, collision_object):
        self.collision_object_types.add(collision_object)

    def update(self):
        self.y_speed = self.y_speed + self.gravity
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def delete_object(self, obj):
        self.room.delete_object(obj)

    def remove_object(self, obj):
        for index, list_obj in enumerate(self.collision_objects):
            if list_obj is obj:
                self.collision_objects.pop(index)

    def step(self):
        pass

    def check_collisions(self):
        for item in self.collision_objects:
            if self.rect.colliderect(item.rect):
                self.handle_collision(item)

    def collides_at(self, obj, x, y, collision_type):
        check_rect = obj.rect.move(x, y)
        collision_found = False
        for item in self.collision_objects:
            if check_rect.colliderect(item.rect):
                if type(item).__name__ == collision_type:
                    collision_found = True
                    break
        return collision_found

    def handle_collision(self, other):
        pass

    def key_pressed(self, key):
        pass

    def clicked(self, button_number):
        pass

    def mouse_event(self, mouse_x, mouse_y, button_left, button_middle, button_right):
        pass

    def bounce(self, other):

        # self is to the side of other
        if other.rect.top < self.rect.centery < other.rect.bottom:
            self.x_speed *= -1
            self.x = self.prev_x

        # self is above or below other
        if other.rect.left < self.rect.centerx < other.rect.right:
            self.y_speed *= -1
            self.y = self.prev_y

    def blocked(self):

        self.x = self.prev_x
        self.y = self.prev_y
        self.x_speed = 0
        self.y_speed = 0

    def set_timer(self, ticks, function_call):
        self.room.set_timer(ticks, function_call)

    def set_direction(self, angle, speed):
        if angle < 0:
            pass
        elif angle == 0:
            self.x_speed = speed
            self.y_speed = 0
        elif angle < 90:
            self.x_speed, self.y_speed = self.get_direction(angle, speed)
        elif angle == 90:
            self.x_speed = 0
            self.y_speed = speed
        elif angle < 180:
            self.x_speed, self.y_speed = self.get_direction(angle - 90, speed)
            self.x_speed, self.y_speed = -self.y_speed, self.x_speed
        elif angle == 180:
            self.x_speed = -speed
            self.y_speed = 0
        elif angle < 270:
            self.x_speed, self.y_speed = self.get_direction(angle - 180, speed)
            self.x_speed, self.y_speed = -self.x_speed, -self.y_speed
        elif angle == 270:
            self.x_speed = 0
            self.y_speed = -speed
        elif angle < 360:
            self.x_speed, self.y_speed = self.get_direction(angle - 270, speed)
            self.x_speed, self.y_speed = self.y_speed, -self.x_speed

    def get_direction(self, angle, speed):
        # Use Trigonometry to calculate x_speed and y_speed values
        new_x_speed = math.cos(math.radians(angle)) * speed
        new_y_speed = math.sin(math.radians(angle)) * speed

        return round(new_x_speed), round(new_y_speed)

    def get_direction_coordinates(self, angle, speed):

        angle += 90
        if angle >= 360:
            angle = angle - 360

        if angle < 0:
            angle = 360 + angle

        if angle == 0:
            x = speed
            y = 0
        elif angle < 90:
            x, y = self.get_direction(angle + 90, speed)
            x, y = y, x
        elif angle == 90:
            x = 0
            y = -speed
        elif angle < 180:
            x, y = self.get_direction(angle, speed)
            y *= -1
        elif angle == 180:
            x = -speed
            y = 0
        elif angle < 270:
            x, y = self.get_direction(angle - 90, speed)
            y, x = -x, -y
        elif angle == 270:
            x = 0
            y = speed
        elif angle < 360:
            x, y = self.get_direction(angle - 180, speed)
            y, x = y, -x

        return x, y

    def rotate(self, angle):

        self.curr_rotation%=360

        self.curr_rotation = self.angle = angle + self.curr_rotation
        
        x, y = self.rect.center

        # start code for creating a rotation of the rect, but not the surface   # mostly 4000ns to 10000ns.
        angle = math.radians((self.angle)%90)
        # width = height = self.width*(math.sin(angle)+math.cos(angle)) # only works for squares, see https://math.stackexchange.com/questions/828878/calculate-dimensions-of-square-inside-a-rotated-square#:~:text=The%20answer%20is%20surprisingly%20simple,0%20and%20%CF%80%2F2%20radians.
        width = self.width*math.cos(angle) + self.height*math.sin(angle)
        height = self.width*math.sin(angle) + self.height*math.cos(angle)
        self.rect = pygame.Rect(0,0,width,height) # constructing rect: 2000ns to 5000ns
        # end of additional code for rotating

        self.x = x - int((self.rect.width / 2))
        self.y = y - int((self.rect.height / 2))       

        self.rect.x = self.x
        self.rect.y = self.y
        

    def get_rotation_to_coordinate(self, target_x, target_y):
        distance_x = self.x + (self.width / 2) - target_x
        distance_y = self.y + (self.height / 2) - target_y

        return math.degrees(math.atan2(distance_x, distance_y))

    def rotate_to_coordinate(self, target_x, target_y):
        self.curr_rotation = 0
        self.rotate(self.get_rotation_to_coordinate(target_x, target_y))

    def get_position(self):
        return self.x, self.y

    def move_in_direction(self, angle, distance):
        x, y = self.get_direction_coordinates(angle, distance)
        self.x += x
        self.y += y

    def point_to_point_distance(self, x1, y1, x2, y2):
        return math.dist((x1,y1), (x2, y2))

