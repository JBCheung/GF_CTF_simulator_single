from GameFrame import Level, Globals, RedFlag, BlueFlag, TextObject


class Arena(Level):
    def __init__(self):
        Level.__init__(self)
        from Objects import DangerZone
        from Objects import Red1, Red2, Red3, Red4, Red5
        from Objects import Blue1, Blue2, Blue3, Blue4, Blue5

        Globals.red_bots.append(Red1(self, Globals.SCREEN_WIDTH - 250, Globals.SCREEN_HEIGHT / 4))
        Globals.blue_bots.append(Blue1(self, 108, Globals.SCREEN_HEIGHT / 3))
        Globals.red_bots.append(Red2(self, Globals.SCREEN_WIDTH - 250, Globals.SCREEN_HEIGHT / 4 * 2))
        Globals.blue_bots.append(Blue2(self, 108, Globals.SCREEN_HEIGHT / 3 * 2))
        Globals.red_bots.append(Red3(self, Globals.SCREEN_WIDTH - 250, Globals.SCREEN_HEIGHT / 4 * 3))
        Globals.blue_bots.append(Blue3(self, 228, Globals.SCREEN_HEIGHT / 4))
        Globals.red_bots.append(Red4(self, Globals.SCREEN_WIDTH - 140, Globals.SCREEN_HEIGHT / 3))
        Globals.blue_bots.append(Blue4(self, 228, Globals.SCREEN_HEIGHT / 4 * 2))
        Globals.red_bots.append(Red5(self, Globals.SCREEN_WIDTH - 140, Globals.SCREEN_HEIGHT / 3 * 2))
        Globals.blue_bots.append(Blue5(self, 228, Globals.SCREEN_HEIGHT / 4 * 3))

        for i in range(len(Globals.red_bots)):
            self.add_room_object(Globals.red_bots[i])

        for i in range(len(Globals.blue_bots)):
            self.add_room_object(Globals.blue_bots[i])

        Globals.red_flag = RedFlag(self, 200, Globals.SCREEN_HEIGHT / 2 - 26)
        Globals.blue_flag = BlueFlag(self, Globals.SCREEN_WIDTH - 232, Globals.SCREEN_HEIGHT / 2 - 26)

        self.add_room_object(Globals.red_flag)
        self.add_room_object(Globals.blue_flag)

        self.red_danger_zone = DangerZone(self, 0, -150)
        self.blue_danger_zone = DangerZone(self, 0, -150)

        self.can_update_red_danger = True
        self.can_update_blue_danger = True

        self.add_room_object(self.red_danger_zone)
        self.add_room_object(self.blue_danger_zone)

        self.counter = 3600
        self.seconds = 120

        self.set_timer(3600, self.timed_out)

    def tick(self):
        self.counter -= 1

        if self.can_update_blue_danger:
            for bot in Globals.blue_bots:
                if bot.point_to_point_distance(bot.x, bot.y, Globals.blue_flag.x, Globals.blue_flag.y) < 50:
                    self.can_update_blue_danger = False
                    self.set_timer(20, self.end_blue_danger)
                    break
        else:
            self.blue_danger_zone.x = Globals.blue_flag.x - 60
            self.blue_danger_zone.y = Globals.blue_flag.y - 60

        if self.can_update_red_danger:
            for bot in Globals.red_bots:
                if bot.point_to_point_distance(bot.x, bot.y, Globals.red_flag.x, Globals.red_flag.y) < 50:
                    self.can_update_red_danger = False
                    self.set_timer(20, self.end_red_danger)
                    break
        else:
            self.red_danger_zone.x = Globals.red_flag.x - 60
            self.red_danger_zone.y = Globals.red_flag.y - 60

    def end_blue_danger(self):
        self.blue_danger_zone.y = -150
        self.can_update_blue_danger = True

    def end_red_danger(self):
        self.red_danger_zone.y = -150
        self.can_update_red_danger = True

    def timed_out(self):
        if Globals.red_enemy_side_time > Globals.blue_enemy_side_time:
            Globals.winner = 'Red'
        elif Globals.blue_enemy_side_time > Globals.red_enemy_side_time:
            Globals.winner = 'Blue'
        else:
            Globals.winner = 'Draw'
        self.running = False

