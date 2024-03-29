from asyncio.windows_events import NULL
import pygame
import random
import setup_Q_table
import math
import csv
import numpy as np

# TRAINING STUFF
EPISODE_NUM = 0
def incrementEpisodeNum():
    global EPISODE_NUM
    EPISODE_NUM = EPISODE_NUM+1
COUNT = 0
def incrementCountNum():
    global COUNT
    COUNT = COUNT+1
def resetCount():
    global COUNT
    COUNT = 0
PREV_DIRECTION = NULL
def changeDirection(dir):
    global PREV_DIRECTION
    PREV_DIRECTION = dir
Q_TABLE = setup_Q_table.make_q_table()
LEARNING_RATE = .2
EPISLON = .9
DISCOUNT_FACTOR = .9
D = .975

MAX_SCORE = 0
def updateScore(num):
    global MAX_SCORE
    if (num > MAX_SCORE):
        MAX_SCORE = num

# Runs on a modified version of Edureka's snake game
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 
 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Generates state of game based on surrounding walls,
# current direction of snake, and food location in 
# relation to the current position of the head of 
# the snake
def get_state(food_x, food_y, snake_x, snake_y, snake_x_change, snake_y_change, snake_list):
    state = [False] * 12
    #Wall/body left
    if (snake_x - snake_block < 0 or snake_list.count([snake_x - snake_block, snake_y]) == 1):
        state[0] = True
    #Wall/body right
    if (snake_x + snake_block >= dis_width or snake_list.count([snake_x + snake_block, snake_y]) == 1):
        state[1] = True
    #Wall/body up
    if (snake_y - snake_block < 0 or snake_list.count([snake_x, snake_y - snake_block]) == 1):
        state[2] = True
    #Wall/body down
    if (snake_y + snake_block >= dis_height or snake_list.count([snake_x, snake_y + snake_block]) == 1):
        state[3] = True

    #Moving left
    if (snake_x_change < 0):
        state[4] = True
    #Moving right
    if (snake_x_change > 0):
        state[5] = True
    #Moving up
    if (snake_y_change < 0):
        state[6] = True
    #Moving down
    if (snake_y_change > 0):
        state[7] = True

    #Food left
    if (food_x < snake_x):
        state[8] = True
    #Food right
    if (food_x > snake_x):
        state[9] = True
    #Food up 
    if (food_y < snake_y):
        state[10] = True
    #Food down
    if (food_y > snake_y):
        state[11] = True
    return state

#Distance from snake to food, used in reward
def get_distance(food_x, food_y, snake_x, snake_y):
    return (math.dist([food_x, food_y],[snake_x, snake_y]))

def chooseAction(curr_state):
    #Chooses random move or max value move based on episode num, lower epi num is exploration
    #Also prevents snake from doubling back on itself
    if (PREV_DIRECTION == NULL):
        r = random.uniform(0,1)
        e = EPISLON * pow(D, EPISODE_NUM)

        if (r > e): #Max move
            action = np.argmax(Q_TABLE[curr_state])
        else:       #Random move
            action = random.randint(0,3)
            
        match action:
            case 0:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
                pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT))
                changeDirection(pygame.K_LEFT)
            case 1:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
                pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))
                changeDirection(pygame.K_RIGHT)
            case 2:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
                pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))
                changeDirection(pygame.K_UP)
            case 3:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
                pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN))
                changeDirection(pygame.K_DOWN)    
    else:
        chosen = False
        while chosen == False:
            r = random.uniform(0,1)
            e = EPISLON * pow(D, EPISODE_NUM)

            if (r > e):
                action = np.argmax(Q_TABLE[curr_state])
            else:
                action = random.randint(0,3)

            match action:
                case 0:
                    if (PREV_DIRECTION != pygame.K_RIGHT):
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT))
                        changeDirection(pygame.K_LEFT)
                        chosen = True
                case 1:
                    if (PREV_DIRECTION != pygame.K_LEFT):
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))
                        changeDirection(pygame.K_RIGHT)
                        chosen = True
                case 2:
                    if (PREV_DIRECTION != pygame.K_DOWN):
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))
                        changeDirection(pygame.K_UP)
                        chosen = True
                case 3:
                    if (PREV_DIRECTION != pygame.K_UP):
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN))
                        changeDirection(pygame.K_DOWN)
                        chosen = True
    return action

def gameLoop():
    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        if (game_close == True):
            updateScore(Length_of_snake - 1)
            incrementEpisodeNum()
            resetCount()
            if EPISODE_NUM < 299:
                gameLoop()
            if EPISODE_NUM == 299:
                input()
                gameLoop()
                
            else:
                print("DONE WITH TRAINING")
                game_over = True
                game_close = False
                print("MAX SCORE:")
                print(MAX_SCORE)
                w = csv.writer(open("output.csv", "w"))
                for key, val in Q_TABLE.items():
                    w.writerow([key, val])
                break

        #Gets current state and distance, will be used at the end to calc reward
        curr_state = tuple(get_state(foodx, foody, x1, y1, x1_change, y1_change, snake_List))
        curr_dist = get_distance(foodx, foody, x1, y1)
        reward = 0

        action = chooseAction(curr_state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        
        #Check for hitting edge
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            #bad reward
            reward -= 100
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        #Check for hitting tail
        for x in snake_List[:-1]:
            if x == snake_Head:
                #bad reward
                reward -= 200
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        #Check for eating food
        if x1 == foodx and y1 == foody:
            #big reward
            reward += 100
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

        new_state = tuple(get_state(foodx, foody, x1, y1, x1_change, y1_change, snake_List))
        new_dist = get_distance(foodx, foody, x1, y1)

        #Small rewards for getting closer
        if (new_dist < curr_dist):
            reward += 1
        if (new_dist > curr_dist):
            reward -= 1
        if (reward < -5):
            print(EPISODE_NUM)
            print("LOST")
        #update q table
        Q_TABLE[curr_state][action] = Q_TABLE[curr_state][action] + LEARNING_RATE * (reward + DISCOUNT_FACTOR * np.max(Q_TABLE[new_state]) - Q_TABLE[curr_state][action])
        
        if COUNT == 3000:
            resetCount()
            print(EPISODE_NUM)
            print("Episode RAN OUT OF TIME")
            game_close = True
        incrementCountNum()

    pygame.quit()
    quit()



if __name__ == "__main__":
    gameLoop()

#TODO: bug where snake eats food, food "under" snake for a frame, snake doesn't know what to do