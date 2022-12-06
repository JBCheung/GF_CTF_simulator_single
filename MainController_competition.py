#!/usr/bin/python3

import os
import time
import shutil
from random import shuffle
from GameFrame import Globals, Simulation_Flags
from Rooms.Arena import Arena
from simulation_results_logger import simulation_results_logger
import multiprocessing

def task_msg(func, msg):
    def inner(*args, **kwargs):
        print(f'{msg}... ', end='')
        value = func(*args, **kwargs)
        print('done')
        return value
    return inner

def load_new_bots():
    index = Globals.current_battle
    Globals.blue_player = Globals.game_list[index][0]
    Globals.red_player = Globals.game_list[index][1]
    for i in range(1, 6):
        source_path = os.path.join('Competitor_Files', Globals.game_list[index][0], 'Blue{}.py'.format(i))
        destination_path = os.path.join('Objects', 'Blue{}.py'.format(i))
        shutil.copy(source_path, destination_path)

        source_path = os.path.join('Competitor_Files', Globals.game_list[index][1], 'Red{}.py'.format(i))
        destination_path = os.path.join('Objects', 'Red{}.py'.format(i))
        shutil.copy(source_path, destination_path)
    Globals.current_battle += 1
def load_game_list():
    # create list of teams to run simulations of
    Globals.players_list = os.listdir(os.path.join('Competitor_Files'))
    curr_player = len(Globals.players_list) - 1
    while curr_player >= 0:
        for adversary in range(0, curr_player):
            Globals.game_list.append((Globals.players_list[curr_player], Globals.players_list[adversary]))
            Globals.game_list.append((Globals.players_list[adversary], Globals.players_list[curr_player]))
        curr_player -= 1
    if Globals.shuffle_gamelist_order:
        shuffle(Globals.game_list)

def simulation(iteration:int, game_list, simulation_logger:multiprocessing.Value, filelock, loggerlock) -> None:
    from GameFrame import Globals
    Globals = Globals.reset_globals(Globals)
    Globals.game_list = game_list
    Globals.current_battle = iteration
    Globals.max_iterations = len(Globals.game_list)
    # copies files for each team to the objects folder for a new match
    if Globals.DEBUG: print(f'{iteration} | pre acquire')
    filelock.acquire()
    if Globals.DEBUG: print(f'{iteration} | post acquire')
    load_new_bots()
    
    start=time.perf_counter()
    room = Arena()
    filelock.release() #load the bot modules before releasing lock
    if Globals.DEBUG: print(f'{iteration} | released')
    Flags = room.run() #start simulation
    end=time.perf_counter()

    realtimetaken = end-start
    #flagsText = f' | {[flag.name for flag in Flags]}' if len(Flags) > 0 else ''
    flagsText = f'{Flags}' if len(Flags) > 0 else ''
    # show statistics so simulation runners know whats happening while the simulation runs (could use multithreading for realtime)
    iteration_no_text = f"{f'{str(iteration+1).zfill(len(str(Globals.max_iterations)))}/{Globals.max_iterations}':{len(str(Globals.max_iterations))*2+1}}"
    fps = (3600-room.counter)/realtimetaken
    print(f"Simulation {iteration_no_text} took {realtimetaken:<18} | FPS:{fps:<18} | Blue:{game_list[iteration][0]:<18} | Red:{game_list[iteration][1]:<18} | {flagsText}")
    
    #handle flags whilst logging data
    loggerlock.acquire()
    logger = simulation_logger.get()
    logger.log_results(room, Globals, Flags, realtimetaken)
    simulation_logger.set(logger)
    loggerlock.release()
    
def main():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' #removes 'welcome to pygame' message for future imports
    start = time.perf_counter()
    print('game list loading... ', end='')
    load_game_list()
    print('done')
    manager = multiprocessing.Manager()
    filelock = manager.Lock()
    loggerlock = manager.Lock()
    # the object used to collect, format, and output results. Using Manager.Value to share the object across processes (simulations)
    simulation_logger = manager.Value(simulation_results_logger, value=simulation_results_logger())
    if Globals.compound_to_previous_data:
        if os.path.exists(os.path.join(os.getcwd(), 'RawResults.json')):
            logger = simulation_logger.get()
            logger.load_data_json() # must be raw data, otherwise values not be updated correctly
            simulation_logger.set(logger)
    def argument_generator(simulation_logger, filelock, loggerlock):
        for i in range(len(Globals.game_list)):
            yield i, Globals.game_list, simulation_logger, filelock, loggerlock
    
    
    print(f'start Pool of {Globals.max_processes} processes | total simulations: {len(Globals.game_list)}')
    with multiprocessing.Pool(Globals.max_processes) as pool:
        pool.starmap(simulation, iterable=argument_generator(simulation_logger, filelock, loggerlock))
    print('waiting for pool to end... ', end='')
    pool.join()
    print('done')


    end = time.perf_counter()
    print('logging results... ', end='')
    simulation_logger.value.output(total_run_time=end-start)
    print('done')
    print(f'total simulation time | {end-start}')        
            
if __name__ == "__main__":
    main()