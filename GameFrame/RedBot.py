from GameFrame import Bot, Globals, RedFlag, Simulation_Flags
import GameFrame.BlueBot


class RedBot(Bot):
    def __init__(self, room, x, y):
        Bot.__init__(self, room, x, y)
        self.set_rect(25, 25)

        self.rotate(90)

        self.register_collision_object('Blue1')
        self.register_collision_object('Blue2')
        self.register_collision_object('Blue3')
        self.register_collision_object('Blue4')
        self.register_collision_object('Blue5')
        self.register_collision_object('RedFlag')
        self.register_collision_object('Red1')
        self.register_collision_object('Red2')
        self.register_collision_object('Red3')
        self.register_collision_object('Red4')
        self.register_collision_object('Red5')

        self.if_cheating_flag = Simulation_Flags.RED_CHEATER

    def frame(self):
        if self.has_flag:
            if self.x < Globals.SCREEN_WIDTH / 2 + Globals.SCREEN_WIDTH / 4:
                Globals.red_flag.x = self.x - Globals.red_flag.rect.width - 2
                Globals.red_flag.y = self.y

                if Globals.red_flag.x <= 0:
                    Globals.red_flag.x = 0

                if Globals.red_flag.y <= 0:
                    Globals.red_flag.y = 0
                elif self.y + Globals.red_flag.rect.height >= Globals.SCREEN_HEIGHT:
                    Globals.red_flag.y = Globals.SCREEN_HEIGHT - Globals.red_flag.rect.height
            else:
                self.has_flag = False

        if self.x < Globals.SCREEN_WIDTH / 2:
            Globals.red_enemy_side_time += 1
            distance = self.point_to_point_distance(self.x, self.y, Globals.red_flag.x, Globals.red_flag.y)
            if self.has_flag:
                Globals.red_enemy_side_time += 50
                self.points += 50
                self.time_with_flag += 1
            elif distance < 50:
                Globals.red_enemy_side_time += 30
                self.points += 30
            elif distance < 150:
                Globals.red_enemy_side_time += 20
                self.points += 20
            elif distance < 250:
                Globals.red_enemy_side_time += 10
                self.points += 10

        try:
            self.tick()
        except Exception as e:
            self.room.flags.add(Simulation_Flags.RED_ERROR)
            self.room.flags.add(e.__repr__())


    def tick(self):
        pass

    def handle_collision(self, other):
        if isinstance(other, RedFlag):
            self.has_flag = True
            for bot in Globals.red_bots:
                if bot.has_flag and bot is not self:
                    self.has_flag = False
                    break
        elif isinstance(other, GameFrame.BlueBot):
            if self.x < Globals.SCREEN_WIDTH / 2 and not other.jailed and not self.jailed:
                self.has_flag = False
                self.curr_rotation = 0
                self.rotate(90)
                self.x = Globals.SCREEN_WIDTH - 36
                self.y = Globals.SCREEN_HEIGHT - 40
                self.jailed = True
                self.deaths+=1
                other.kills+=1
        elif isinstance(other, RedBot):
            if not other.jailed and self.jailed:
                self.jailed = False
                other.friends_released+=1