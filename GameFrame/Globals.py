import math
from enum import Enum
class Globals:
    
    ##########################################################################################
    #### these are for collecting stats of bots and for SPEED! (added stuff in this mod) #####
    ##########################################################################################
    
    #--------------- simulation variables ---------------#
    'necessary variables for running simulations. It is recommended to turn off visual processing when running simulations for data (see "visual/ optimisation")'
    max_iterations = 1 # number of interations run. runs at ~300-350 FPS
    max_processes = 1 #the number of simulations that can be run at the same time. adjust this as per your device's specifications
    
    DEBUG = False

    #----------------- data collection ------------------#
    'these are flags for storing results or not. True if you want the file, False if not'
    
    # output the raw data collected by the simulation_results_logger class to RawResults.json
    generate_results_raw = True
    
    # condenses raw data collected into averages, median, min and max 
    generate_results_detailed = False 
    
    # similar to DetailedResults.json
    generate_results_only_averages = True 
    
    # the simulation_results_logger will record and complile current data 
    # and an existing RawResults.json (add onto previous data) by having MainController.py run a setup method
    compound_to_previous_data = True   
    


    running = True
    FRAMES_PER_SECOND = math.inf
    
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    SCORE = 0

    # - Set the starting number of lives - #
    LIVES = 3

    # - Set the Window display name - #
    window_name = 'GF Capture the Flag'

    # - Set the order of the rooms - #
    levels = ["Arena"]

    red_player = 'Red'

    blue_player = 'Blue'

    players_list = []
    game_list = []
    current_battle = 0

    # - Winner Text - #
    winner = ' '

    # - Set the starting level - #
    start_level = 0

    # - Set this number to the level you want to jump to when the game ends - #
    end_game_level = 1

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

class Simulation_Flags(Enum):
    BLUE_CHEATER=0
    RED_CHEATER=1
    BLUE_ERROR=2
    RED_ERROR=3
