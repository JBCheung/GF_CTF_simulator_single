#!/usr/bin/python3

import os
import time
import shutil
from GameFrame import Globals, Simulation_Flags
from Rooms.Arena import Arena
from simulation_results_logger import simulation_results_logger
import multiprocessing

def simulation(iteration:int, simulation_logger:multiprocessing.Value, loggerlock) -> None:
    from GameFrame import Globals
    Globals = Globals.reset_globals(Globals)
    start=time.perf_counter()
    room = Arena()
    Flags = room.run() #start simulation
    end=time.perf_counter()

    realtimetaken = end-start
    #flagsText = f' | {[flag.name for flag in Flags]}' if len(Flags) > 0 else ''
    flagsText = f'{Flags}' if len(Flags) > 0 else ''
    # show statistics so simulation runners know whats happening while the simulation runs (could use multithreading for realtime)
    iteration_no_text = f"{f'{str(iteration+1).zfill(len(str(Globals.max_iterations)))}/{Globals.max_iterations}':{len(str(Globals.max_iterations))*2+1}}"
    fps = (3600-room.counter)/realtimetaken
    print(f"Simulation {iteration_no_text} took {realtimetaken:<18} | FPS:{fps:<18} | winner: {Globals.winner:<4} | {flagsText}")
    
    #handle flags whilst logging data
    loggerlock.acquire()
    logger = simulation_logger.get()
    logger.log_results(room, Globals, Flags, realtimetaken)
    simulation_logger.set(logger)
    loggerlock.release()
    
def main():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' #removes 'welcome to pygame' message for future imports
    start = time.perf_counter()
    manager = multiprocessing.Manager()
    # lock for processes to access logger
    loggerlock = manager.Lock()
    # the object used to collect, format, and output results. Using Manager.Value to share the object across processes (simulations)
    simulation_logger = manager.Value(simulation_results_logger, value=simulation_results_logger())
    
    if Globals.compound_to_previous_data:
        if os.path.exists(os.path.join(os.getcwd(), 'RawResults.json')):
            logger = simulation_logger.get()
            logger.load_data_json() # must be raw data, otherwise values not be updated correctly
            simulation_logger.set(logger)
    def argument_generator(simulation_logger, loggerlock):
        "a generator for the simulation's arguments"
        for i in range(Globals.max_iterations):
            yield i, simulation_logger, loggerlock
    
    if Globals.max_processes > Globals.max_iterations:
        Globals.max_processes = Globals.max_iterations
    print(f'start Pool of {Globals.max_processes} processes | total simulations: {Globals.max_iterations}')
    with multiprocessing.Pool(Globals.max_processes) as pool:
        pool.starmap(simulation, iterable=argument_generator(simulation_logger, loggerlock))
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