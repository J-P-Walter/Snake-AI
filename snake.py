import pygame
import time
import random
import setup_Q_table
import math
import csv
import numpy as np

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

Q_TABLE = setup_Q_table.make_q_table()

LEARNING_RATE = .2
EPISLON = .9
DISCOUNT_FACTOR = .8
D = .9 #don't know what this is...


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

def get_state(food_x, food_y, snake_x, snake_y, snake_x_change, snake_y_change, snake_list):
    state = [False] * 12

    #Wall left
    if (snake_x - snake_block < 0 or snake_list.count([snake_x - snake_block, snake_y]) == 1):
       # print("wall left")
        state[0] = True
    #Wall right
    if (snake_x + snake_block >= dis_width or snake_list.count([snake_x + snake_block, snake_y]) == 1):
       # print("wall right")
        state[1] = True
    #Wall up
    if (snake_y - snake_block < 0 or snake_list.count([snake_x, snake_y - snake_block]) == 1):
        #print("wall up")
        state[2] = True
    #Wall down
    if (snake_y + snake_block >= dis_height or snake_list.count([snake_x, snake_y + snake_block]) == 1):
        #print("wall down")
        state[3] = True

    #Moving left
    if (snake_x_change < 0):
        #print("moving left")
        state[4] = True
    #Moving right
    if (snake_x_change > 0):
        #print("moving right")
        state[5] = True
    #Moving up
    if (snake_y_change < 0):
        #print("moving up")
        state[6] = True
    #Moving down
    if (snake_y_change > 0):
        #print("moving down")
        state[7] = True

    #Food left
    if (food_x < snake_x):
        #print("food left")
        state[8] = True
    #Food right
    if (food_x > snake_x):
        #print("food right")
        state[9] = True
    #Food up 
    if (food_y < snake_y):
        #print("food up")
        state[10] = True
    #Food down
    if (food_y > snake_y):
        #print("food down")
        state[11] = True
    return state

def get_distance(food_x, food_y, snake_x, snake_y):
    return (math.dist([food_x, food_y],[snake_x, snake_y]))

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
    
    #pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))

    while not game_over:
        if (game_close == True):
            incrementEpisodeNum()
            resetCount()
            if EPISODE_NUM < 20:
                gameLoop()
            if EPISODE_NUM == 20:
                input()
                gameLoop()
                
            else:
                print("DONE WITH TRAINING")
                game_over = True
                game_close = False

                w = csv.writer(open("output.csv", "w"))
                for key, val in Q_TABLE.items():
                    w.writerow([key, val])

                break

        #Gets current state and distance, will be used at the end to calc reward
        curr_state = tuple(get_state(foodx, foody, x1, y1, x1_change, y1_change, snake_List))
        curr_dist = get_distance(foodx, foody, x1, y1)
        reward = 0

        #Chooses random move or max value move based on episode num, lower epi num is exploration
        r = random.uniform(0,1)
        e = EPISLON * pow(D, EPISODE_NUM)

        if (r > e):
            #print("max")
            action = np.argmax(Q_TABLE[curr_state])
        else:
            #print("r")
            action = random.randint(0,3)
        
        match action:
            case 0:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
            case 1:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
            case 2:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
            case 3:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))    

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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            #bad reward
            reward -= 10
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

        for x in snake_List[:-1]:
            if x == snake_Head:
                #bad reward
                reward -= 50
                game_close = True
                print("HIT TAIL")

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            #big reward
            reward += 50
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

        new_state = tuple(get_state(foodx, foody, x1, y1, x1_change, y1_change, snake_List))
        new_dist = get_distance(foodx, foody, x1, y1)

        if (new_dist < curr_dist):
            reward += 1
        if (new_dist > curr_dist):
            reward -= 1
        if (reward > 5):
            print("ATE YUMMY")
        if (reward < -5):
            print(EPISODE_NUM)
            print("LOST")
        #update q table
        Q_TABLE[curr_state][action] = Q_TABLE[curr_state][action] + LEARNING_RATE * (reward + DISCOUNT_FACTOR * np.max(Q_TABLE[new_state]) - Q_TABLE[curr_state][action])
        
        if COUNT == 2000:
            resetCount()
            print(EPISODE_NUM)
            print("Episode RAN OUT OF TIME")
            game_close = True
        incrementCountNum()

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()