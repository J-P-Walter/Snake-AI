from asyncio.windows_events import NULL
import pygame
import random
import numpy as np
import csv
import ast

PREV_DIRECTION = NULL
def changeDirection(dir):
    global PREV_DIRECTION
    PREV_DIRECTION = dir

def readInTable(table_name):
    global Q_TABLE 
    file = open(table_name)
    csvreader = csv.reader(file)

    for row in csvreader:
        if len(row) == 2:
            Q_TABLE[ast.literal_eval(row[0])] = ast.literal_eval(row[1])


Q_TABLE = {}

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
        state[0] = True
    #Wall right
    if (snake_x + snake_block >= dis_width or snake_list.count([snake_x + snake_block, snake_y]) == 1):
        state[1] = True
    #Wall up
    if (snake_y - snake_block < 0 or snake_list.count([snake_x, snake_y - snake_block]) == 1):
        state[2] = True
    #Wall down
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

def chooseAction(curr_state):
    if (PREV_DIRECTION == NULL):
        action = np.argmax(Q_TABLE[tuple(curr_state)])  
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
            action = np.argmax(Q_TABLE[tuple(curr_state)])
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
    readInTable('output.csv')

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
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        #Gets current state and distance, will be used at the end to calc reward
        curr_state = tuple(get_state(foodx, foody, x1, y1, x1_change, y1_change, snake_List))

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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
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
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()



if __name__ == "__main__":
    gameLoop()
