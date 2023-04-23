# SNAKE AI using Q-Learning

Ran for 300 episodes with a 3000 move cutoff. The snake never ran out of moves as the game ended before then, and eventually got pretty good so the last 100 or so took a while. Highest score achieved while training was 71.

snake.py generates a new, empty Q-Table and runs the game for a variable number of episodes, episode length, learning rate, etc. and outputs the generated Q-Table as a CSV file to be used by final_snake.py
final_snake.py takes a Q-Table as a csv and runs based only on the best choice from said table. 

![image](https://user-images.githubusercontent.com/70927525/233860699-cd756fc5-cb8a-451d-a376-8ff6baab41cd.png)
