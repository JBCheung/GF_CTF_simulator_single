#!/usr/bin/python3

import os
import time
import pygame
import shutil
from GameFrame import Globals, Simulation_Flags
from Rooms.Arena import Arena
from simulation_results_logger import simulation_results_logger
import multiprocessing

def simulation(iteration:int, simulation_logger:multiprocessing.Value, loggerlock) -> None:
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
    
    #logging data and acquiring lock before doing so
    loggerlock.acquire()
    logger = simulation_logger.value
    logger.log_results(room, realtimetaken)
    simulation_logger.value = logger
    loggerlock.release()
    

def main():
    start = time.perf_counter()
    Globals.next_level = Globals.start_level
    levels = Globals.levels
    manager = multiprocessing.Manager()
    loggerlock = manager.Lock()
    # the object used to collect, format, and output results. Using Manager.Value to share the object across processes (simulations)
    simulation_logger = manager.Value(simulation_results_logger, value=simulation_results_logger())
    if Globals.compound_to_previous_data:
        if os.path.exists(os.path.join(os.getcwd(), 'RawResults.json')):
            simulation_logger.value.load_data_json() # must be raw data, otherwise values not be updated correctly

    def argument_generator(simulation_logger, loggerlock):
        for i in range(Globals.max_iterations):
            yield i, simulation_logger, loggerlock
    
    print('start Pool/ processes')
    with multiprocessing.Pool(Globals.max_processes) as pool:
        pool.starmap(simulation, iterable=argument_generator(simulation_logger, loggerlock))
    print('waiting for pool to end')
    pool.join()
    print('pool ended')


    end = time.perf_counter()
    print('logging results')
    simulation_logger.value.output(total_run_time=end-start)
    print('logging results finished')
    print(f'total simulation time | {end-start}')        
            
if __name__ == "__main__":
    main()