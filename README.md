SNAKE AI

Project using Q-Learning since my code for the HCR assignment didn't seem to work. 

Can absolutely be optimized in some way, probably by tweaking the numbers a bit. I ran for 300 episodes with a 3000 move cutoff. The snake never ran out of moves and
eventually got pretty good so the last 100 or so took a while. Highest score achieved while training was 71.

snake.py generates a new, empty Q-Table and runs the game for a variable number of episodes, episode length, learning rate, etc. and outputs the generated Q-Table as a CSV file
final_snake.py takes a Q-Table as a csv and runs based only on the best choice from said table
