import math
from enum import Enum
class Globals:
    
    ##########################################################################################
    #### these are for collecting stats of bots and for SPEED! (added stuff in this mod) #####
    ##########################################################################################
    
    #--------------- simulation settings ---------------#
    'necessary settings for running simulations.'
    max_iterations = 1 # number of simulations to run. Overwritten by competition version to be the length of game_list
    max_processes = 5 #the number of simulations that can be run at the same time. adjust this as per your device's specifications
    
    DEBUG = False
    shuffle_gamelist_order = False
    
    #----------------- data collection settings ------------------#
    'these are flags for storing results or not. True if you want the file, False if not'
    
    # output the raw data collected by the simulation_results_logger class to RawResults.json
    generate_results_raw = True
    
    # creates averages of lists, then outputs to results.json
    generate_results = True 

    # competition results - NOT IMPLEMENTED
    generate_results_ranking = True

    # condenses raw data collected into averages, median, min and max (outputs to ) - NOT IMPLEMENTED
    generate_results_statistics = False 

    # the simulation_results_logger will record and complile current data 
    # and an existing RawResults.json (add onto previous data) by having MainController.py run a setup method
    compound_to_previous_data = False   
    
    
    #----------------- dynamic globals/ constants ------------------#
    'required for GameFrame to run'
    running = True
    # FRAMES_PER_SECOND = math.inf
    
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # - Set the order of the rooms - #
    levels = ["Arena"]

    red_player = 'Red'

    blue_player = 'Blue'

    players_list = []
    game_list = []
    current_battle = 0

    # - Winner Text - #
    winner = ' '

    # # - Set the starting level - #
    # start_level = 0

    # # - Set this number to the level you want to jump to when the game ends - #
    # end_game_level = 1

    # - Change variable to True to exit the program - #
    exiting = False

    # bot lists
    red_bots = []
    blue_bots = []

    # Flags
    red_flag = 0
    blue_flag = 0

    # Speeds
    SLOW = 2
    MEDIUM = 5
    FAST = 8

    # Direction
    LEFT = 0
    RIGHT = 1

    # Time in opposition half
    red_enemy_side_time = 0
    blue_enemy_side_time = 0

    def reset_globals(Globals):
        Globals.red_player = 'Red'
        Globals.blue_player = 'Blue'
        Globals.winner=''
        Globals.running = True
        Globals.exiting = False
        Globals.red_bots=[]
        Globals.blue_bots=[]
        Globals.blue_enemy_side_time=0
        Globals.red_enemy_side_time=0
        Globals.red_flag=0
        Globals.blue_flag=0
        return Globals

class Simulation_Flags(Enum):
    BLUE_CHEATER=0
    RED_CHEATER=1
    BLUE_ERROR=2
    RED_ERROR=3
