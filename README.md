# GF_Capture_The_Flag simulator
Capture the flag environment using GameFrame
This version contains both the competition MainController and the MainController that only runs one set of bots.
WARNING:
Do not run the competition runner with your bots in the Objects folder. The Objects folder is where your bots must be to run MainController_single.py, however MainController_competition.py will overwrite the bots there. Therefore, you should be careful when both MainControllers are open. 

Main differences from original GF Capture The Flag:
+ allows multiple simulations to be run back to back
+ supports multiprocessing
+ adds json files with the statistics of each bot and the overall simulation
+ can detect cheating
- doesn't support screen/ visuals
