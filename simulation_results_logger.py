from GameFrame import Globals
import json
import statistics


class simulation_results_logger():
    def __init__(self)-> None:
        # self.data is a dict of the names of the bots (blue1, blue2, red1, red2 etc.) as keys and dictionary of their data as their value
        # the dictionary for each bot contains specific stats like points won, deaths, etc, values stored in lists so averages can be taken 
        '''
        {
            'overall'{
                'bluepoints':[23121, 12345, 54231 ...],
                'redpoints': [78901, 79809, 79809 ...],
                'bluewin_timeleft': [45, 0, 12, 53 ...],
                'redwin_timeleft':  [23, 12, 42, 0 ...],
            },
            
            'blue1': {
                'points': [10310, 12412, 8031, 4712, 9982 ...],
                ...
            },
            'blue2': {...},
            ...
            
        }
        '''
        
        self.data = {
            'overall': {
                'blue_points':[],
                'red_points': [],
                'blue_wins':0,
                'red_wins':0,
                'draws':0,
                'bluewin_timeleft': [],
                'redwin_timeleft': [],
                'timeleft':[],    
                'time_per_simulation': [],
                'simulations_run':0,
                'total_run_time':0,
                #'time_per_tick':[], # implement this
                'ticks_per_second':[], # implement this
            },
        }
        
    def load_data_json(self):
        with open('RawResults.json','r') as file:
            data = json.load(file)
            self.data.update(data)

            
    
    def log_results(self, arena, simulation_time):
        '''
        logs the data of the bots 
        '''
        ticksleft = arena.counter
        ticksElapsed = 3600-ticksleft
        
        self.data['overall']['simulations_run']+=1
        self.data['overall']['total_run_time']+= simulation_time

        self.data['overall']['ticks_per_second'].append(ticksElapsed/simulation_time)
        
        all_bots = Globals.blue_bots.copy()
        all_bots.extend(Globals.red_bots)
        
        for bot in all_bots:
            name = str(type(bot).__name__)
            self.data[name] = self.data.get(name, {})
            if len(self.data[name]) <= 0:
                self.data[name] = {
            'description':bot.tick.__doc__,
            'points':[bot.points],
            'time_with_flag':[bot.time_with_flag],
            'kills':[bot.kills],
            'deaths':[bot.deaths],
            'friends_released':[bot.friends_released],
            }
            else:
                self.data[name]['description'] = bot.tick.__doc__
                self.data[name]['points'].append(bot.points)
                self.data[name]['time_with_flag'].append(bot.time_with_flag)
                self.data[name]['kills'].append(bot.kills)
                self.data[name]['deaths'].append(bot.deaths)
                self.data[name]['friends_released'].append(bot.friends_released)
            
            
        self.data['overall']['time_per_simulation'].append(simulation_time)
            
        self.data['overall']['blue_points'].append(Globals.blue_enemy_side_time)
        self.data['overall']['red_points'].append(Globals.red_enemy_side_time)
        self.data['overall']['timeleft'].append(ticksleft)
        if Globals.red_enemy_side_time > Globals.blue_enemy_side_time:
            self.data['overall']['red_wins'] += 1
            self.data['overall']['redwin_timeleft'].append(ticksleft)
        elif Globals.red_enemy_side_time < Globals.blue_enemy_side_time:
            self.data['overall']['blue_wins'] += 1
            self.data['overall']['bluewin_timeleft'].append(ticksleft)
        else:
            self.data['overall']['draws'] +=1
        
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

    def output(self, total_run_time):
        self.data['overall']['total_run_time'] = total_run_time
        if Globals.generate_results_raw:
            with open('RawResults.json', 'w') as file:
                json.dump(self.data,file,indent=4)


        self.data['overall']['total_run_time'] = self.secondstotime(self.data['overall']['total_run_time'], show_hours=True)
        if Globals.generate_results_detailed:
            detailed = self.data.copy()
            for key1 in self.data:
                for key2, value in self.data[key1].items():
                    if isinstance(value, list): # find averages, median, min, max
                        if len(value) <= 0:
                            self.data[key1][key2] = None
                        elif 'timeleft' in key2:
                            detailed[key1][key2] = {
                                'avg':self.tickstotime(statistics.mean(value)),
                                'median':self.tickstotime(statistics.median(value)),
                                'min':self.tickstotime(min(value)),
                                'max':self.tickstotime(max(value))
                            }
                            # self.data[key1][f'{key2}_avg'] = self.tickstotime(statistics.mean(value))
                            # self.data[key1][f'{key2}_median'] = self.tickstotime(statistics.median(value))
                            # self.data[key1][f'{key2}_min'] = self.tickstotime(min(value))
                            # self.data[key1][f'{key2}_max'] = self.tickstotime(max(value))
                        else:
                            detailed[key1][key2] = {
                                'avg':statistics.mean(value),
                                'median':statistics.median(value),
                                'min':min(value),
                                'max':max(value)
                            }
                            # self.data[key1][f'{key2}_avg'] = statistics.mean(value)
                            # self.data[key1][f'{key2}_median'] = statistics.median(value)
                            # self.data[key1][f'{key2}_min'] = min(value)
                            # self.data[key1][f'{key2}_max'] = max(value)
            # end forloop          
            with open('StatisticsResults.json', 'w') as file:
                json.dump(detailed, file, indent=4)
        #end if

        if Globals.generate_results_only_averages:
            for key1 in self.data:
                for key2, value in self.data[key1].items():
                    if isinstance(value, list): # find averages, median, min, max
                        if len(value) <= 0:
                            self.data[key1][key2] = None
                        elif 'timeleft' in key2:
                            self.data[key1][key2] = self.tickstotime(statistics.mean(value))
                        else:
                            self.data[key1][key2] = statistics.mean(value)     
            with open('Results.json', 'w') as file:
                json.dump(self.data, file, indent=4)
                    
            # adjust ticks to time (30 ticks = 1 second: with 2 minutes each game)
            # self.data['overall']['redwin_timeleft'] = self.ticks_to_formattedtime(self.data['overall']['redwin_timeleft'])
            # self.data['overall']['bluewin_timeleft'] = self.ticks_to_formattedtime(self.data['overall']['bluewin_timeleft'])
            # self.data['overall']['timeleft'] = self.ticks_to_formattedtime(self.data['overall']['timeleft'])
