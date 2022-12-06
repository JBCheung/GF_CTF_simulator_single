from GameFrame import Globals, Simulation_Flags
import json
import statistics


class simulation_results_logger():
    def __init__(self)-> None:
        self.data = {
            'overall': {
                'time_per_simulation': [],
                'simulations_run':0,
                'total_run_time':0,
                #'time_per_tick':[], # implement this
                'ticks_per_second':[],
            },
        }
    
    def log_team(self, bots, teamName, ticksleft, team_colour, points, extra_info={}):
            self.data[teamName] = self.data.get(teamName, {})
            self._log_overall_team_results(teamName, ticksleft, team_colour, points)
            self.data[teamName]['overall'].update(extra_info)
            for bot in bots:
                self._log_bot(bot,teamName)
    def _log_overall_team_results(self, teamName, ticksleft, team_colour, points):
        team_overall = self.data[teamName].get('overall', {})
        if len(team_overall) <= 0:
                team_overall = {
            'average_points':[],
            'total_wins':0,
            'draws':0,
            'red_wins':0,
            'redwin_timeleft':[],
            'blue_wins':0,
            'bluewin_timeleft':[],
            'games_played':0
            }
        team_overall['games_played'] += 1   
        team_overall['average_points'].append(points)             
        if team_colour == 'red' and (Globals.red_enemy_side_time > Globals.blue_enemy_side_time):
            team_overall['red_wins'] += 1
            team_overall['total_wins'] += 1
            team_overall['redwin_timeleft'].append(ticksleft)
        elif team_colour == 'blue' and (Globals.red_enemy_side_time < Globals.blue_enemy_side_time):
            team_overall['blue_wins'] += 1
            team_overall['total_wins'] += 1
            team_overall['bluewin_timeleft'].append(ticksleft)
        elif (Globals.red_enemy_side_time == Globals.blue_enemy_side_time):
            team_overall['draws'] +=1
        self.data[teamName]['overall'] = team_overall    
    def _log_bot(self, bot, teamName):
        name = str(type(bot).__name__)
        bot_data = self.data[teamName][name] = self.data.get(teamName, {}).get(name, {})
        if len(bot_data) <= 0:
                bot_data = {
            'description':bot.tick.__doc__,
            'points':[bot.points],
            'time_with_flag':[bot.time_with_flag],
            'kills':[bot.kills],
            'deaths':[bot.deaths],
            'friends_released':[bot.friends_released],
            }
        else:
            bot_data['description'] = bot.tick.__doc__
            bot_data['points'].append(bot.points)
            bot_data['time_with_flag'].append(bot.time_with_flag)
            bot_data['kills'].append(bot.kills)
            bot_data['deaths'].append(bot.deaths)
            bot_data['friends_released'].append(bot.friends_released)
        self.data[teamName][name] = bot_data
    def log_simulation_overall(self, arena, simulation_time):
        ticksleft = arena.counter
        ticksElapsed = 3600-ticksleft
        self.data['overall']['simulations_run'] = self.data['overall'].get('simulations_run',0)+1
        self.data['overall']['total_run_time'] = self.data['overall'].get('total_run_time',0)+simulation_time
        self.data['overall']['ticks_per_second'] = self.data['overall'].get('ticks_per_second',[])
        self.data['overall']['ticks_per_second'].append(ticksElapsed/simulation_time)
        self.data['overall']['time_per_simulation'] = self.data['overall'].get('time_per_simulation',[])
        self.data['overall']['time_per_simulation'].append(simulation_time)
    def log_results(self, arena, Globals:Globals, Flags:list, simulation_time):
        '''logs the data of the bots '''
        ticksleft = arena.counter
        red_cheating = Simulation_Flags.RED_CHEATER in Flags
        red_error = Simulation_Flags.RED_ERROR in Flags
        blue_cheating = Simulation_Flags.BLUE_CHEATER in Flags
        blue_error = Simulation_Flags.BLUE_ERROR in Flags
        blue_extrainfo = {
            'cheating':blue_cheating, 
            'error_occurred':blue_error
        }
        red_extrainfo = {
            'cheating':red_cheating, 
            'error_occurred':red_error
        }
        if not red_cheating:
            self.log_team(Globals.blue_bots, Globals.blue_player, ticksleft, team_colour='blue', points=Globals.blue_enemy_side_time, extra_info=blue_extrainfo)
        if not blue_cheating:
            self.log_team(Globals.red_bots, Globals.red_player, ticksleft, team_colour='red', points=Globals.red_enemy_side_time, extra_info=red_extrainfo)
        self.log_simulation_overall(arena, simulation_time)
        pass

    def output(self, total_run_time):
        self.data['overall']['total_run_time'] = total_run_time
        if Globals.generate_results_raw:
            with open('RawResults.json', 'w') as file:
                json.dump(self.data,file,indent=4)

        self.data['overall']['total_run_time'] = self.secondstotime(self.data['overall']['total_run_time'], show_hours=True)
        if Globals.generate_results_statistics:
            pass
            '''detailed = self.data.copy()   
            with open('StatisticsResults.json', 'w') as file:
                json.dump(detailed, file, indent=4)'''
        #end if

        if Globals.generate_results:
            self.data = self._simplify_results(self.data)   
            with open('Results.json', 'w') as file:
                json.dump(self.data, file, indent=4)

    def _simplify_results(self,data:dict) -> dict:
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self._simplify_results(value)
            elif isinstance(value, list):
                if len(value) <= 0:
                    data[key] = None
                elif 'timeleft' in key:
                    data[key] = self.tickstotime(statistics.mean(value))
                else:
                    data[key] = statistics.mean(value)
        return data
    def load_data_json(self):
        with open('RawResults.json','r') as file:
            data = json.load(file)
            self.data.update(data)
    def tickstotime(self, ticks, ticks_in_second=30, hours=False) -> str:
        '''
        converts to f'{minutes}:{seconds}'
        
        converts to f'{hours}:{minutes}:{seconds}' if hours=True
        '''
        seconds = ticks/ticks_in_second
        return self.secondstotime(seconds, show_hours=hours)
    @staticmethod
    def secondstotime(seconds, show_hours=False):
        hours = int((seconds)//3600)
        minutes = int((seconds)//60)
        seconds = int((seconds)%60)
        return f'{hours}:{int(minutes%60)}:{seconds}' if show_hours else f'{int(minutes)}:{seconds}'
