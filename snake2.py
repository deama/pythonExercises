import sys
import time
import random
from threading import Timer
from pynput import keyboard
from os import system, name 
from time import sleep 

gridLayout = [[]]
snake = [[9,8],[9,9],[9,10],[9,11]]

refresh = 0.1
snakeSpeed = 0.1
fruitSpawnTime = 5

gridSymbol = 0
fruitSymbol = "#"

snakeHeadSymbol = "+"
snakeTailSymbol = "="

direction = [0] #0 = up, 1 = down, 2 = left, 3 = right
score = [0]
runGame = [0] #0 = run, 1 = stop





#KEY LISTENER-----------------------------------------------------
COMBINATIONS = [
    {keyboard.Key.up},
    {keyboard.Key.down},
    {keyboard.Key.left},
    {keyboard.Key.right}
]

current = set()

def execute(key):
    if key == keyboard.Key.up:
        direction[0] = 0
    elif key == keyboard.Key.down:
        direction[0] = 1
    elif key == keyboard.Key.left:
        direction[0] = 2
    elif key == keyboard.Key.right:
        direction[0] = 3

def on_press(key):
    if runGame[0] != 0:
        return False
    
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute(key)

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
#KEY LISTENER END-----------------------------------------------------






#Threads----------------------------------------------------------------
def refreshCycle(): #thread
    snakeDraw() #just once
    while runGame[0] == 0:
        grid = "\n"
        for i, row in enumerate(gridLayout):
            for cell in row:
                grid = grid + str(cell)
            grid = grid + "\n"
        clear()
        sys.stdout.write( "Score: " + str(score[0]) )
        sys.stdout.write(grid)
        time.sleep(refresh)
    return

def snakeMovement(): #thread
    try:
        storeOld = [0,0]
        storeOld2 = [0,0]
        while runGame[0] == 0:
            storeOld[0] = snake[0][0]
            storeOld[1] = snake[0][1]
            if direction[0] == 0:
                snake[0][0] = snake[0][0] - 1
            elif direction[0] == 1:
                snake[0][0] = snake[0][0] + 1
            elif direction[0] == 2:
                snake[0][1] = snake[0][1] - 1
            elif direction[0] == 3:
                snake[0][1] = snake[0][1] + 1

            if gridLayout[ snake[0][0] ][ snake[0][1] ] == fruitSymbol:
                snake.append([0,0])
                score[0] = score[0] + 1

            for i in range( 1, len(snake) ):
                storeOld2[0] = snake[i][0]
                storeOld2[1] = snake[i][1]
                snake[i][0] = storeOld[0]
                snake[i][1] = storeOld[1]
                storeOld[0] = storeOld2[0]
                storeOld[1] = storeOld2[1]

            snakeDraw()
                    
            gridLayout[ snake[len(snake)-1][0] ][ snake[len(snake)-1][1] ] = gridSymbol
            
            time.sleep(snakeSpeed)
    except:
        runGame[0] = 1
    return


def fruit():
    while runGame[0] == 0:
        try:
            x = random.randint(0, len(gridLayout)-1)
            y = random.randint(0, len(gridLayout[0])-1)
        except:
            #bad random generation
            sys.stdout.write("BAD RANDOM:", x,y)
            pass

        gridLayout[x][y] = fruitSymbol

        time.sleep(fruitSpawnTime)
    return

#Threads END------------------------------------------------------------





        
#Functions--------------------------------------------------------------
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def snakeDraw():
    for i in range( len(snake)-1 ): #-1 maybe error?
        if i == 0:
            gridLayout[snake[i][0]][snake[i][1]] = snakeHeadSymbol #head
        else:
            gridLayout[snake[i][0]][snake[i][1]] = snakeTailSymbol #tail

def main():
    for i in range(0, 20): #y
        gridLayout.append([])
        for p in range(0,30): #X
            gridLayout[i].append(gridSymbol)
    
    thread1 = Timer( refresh, refreshCycle )#repeatedly prints arena
    thread1.start()

    thread2 = Timer( refresh*5, snakeMovement )#moves snake around arena
    thread2.start()

    thread3 = Timer( refresh*10, fruit )
    thread3.start()

    #Main thread starts listening for keys
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
#Functions END-----------------------------------------------------------

main()
sys.stdout.write("GAME OVER")
