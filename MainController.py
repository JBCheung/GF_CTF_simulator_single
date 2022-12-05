#!/usr/bin/python3


def main():
    import os
    import time
    import pygame
    from GameFrame import Globals
    from Rooms.Arena import Arena
    from simulation_results_logger import simulation_results_logger
    
    start_main=time.perf_counter()
    Globals.next_level = Globals.start_level
    levels = Globals.levels
    

    # the object used to collect, format, and output results
    simulation_logger = simulation_results_logger()
    if Globals.compound_to_previous_data:
        if os.path.exists(os.path.join(os.getcwd(), 'RawResults.json')):
            simulation_logger.load_data_json() # must be raw data, otherwise values not be updated correctly
    
    
    for iteration in range(0,Globals.max_iterations):
        # resetting Globals for new simulation
        Globals.running = True
        Globals.exiting = False
        Globals.red_bots=[]
        Globals.blue_bots=[]
        Globals.blue_enemy_side_time=0
        Globals.red_enemy_side_time=0
        Globals.red_flag=0
        Globals.blue_flag=0
        
        
        try:
            room = Arena()
            start=time.perf_counter()
            exit_val = room.run()
            end=time.perf_counter()
            realtimetaken = end-start
            # show statistics so simulation runners know whats happening while the simulation runs (could use multithreading for realtime)
            iteration_no_text = f'{str(iteration+1).zfill(len(str(Globals.max_iterations)))}/{Globals.max_iterations}'
            fps = (3600-room.counter)/realtimetaken
            print(f"Simulation {iteration_no_text} took {realtimetaken} | FPS:{fps}")
            # after game ended, log results
            simulation_logger.log_results(room, realtimetaken)
        except KeyboardInterrupt: # allows for simulations to be interupted without losing previously logged data
            break
    end_main=time.perf_counter()
    print(f'simulation took: {end_main-start_main}')
    simulation_logger.output(total_run_time=end_main-start_main)
        
            
            
if __name__ == "__main__":
    main()