import time
import random
from threading import Timer
import keyboard
from time import sleep 

gridLayout = [[]]
snake = [[9,8],[9,9],[9,10],[9,11]]

refresh = 0.05
snakeSpeed = 0.1
fruitSpawnTime = 3

gridSymbol = "#"
fruitSymbol = "@"

snakeHeadSymbol = "+"
snakeTailSymbol = "="

direction = [0] #0 = up, 1 = down, 2 = left, 3 = right
score = [0]
runGame = [0] #0 = run, 1 = stop







#Threads----------------------------------------------------------------
def refreshCycle(): #thread
    snakeDraw() #just once
    while runGame[0] == 0:
        grid = "\n"
        for i, row in enumerate(gridLayout):
            for cell in row:
                if cell == snakeHeadSymbol or cell == snakeTailSymbol:
                    grid = grid + "\033[91m" + str(cell) + "\033[00m"
                elif cell == fruitSymbol:
                    grid = grid + "\033[93m" + str(cell) + "\033[00m"
                else:
                    grid = grid + str(cell)
            grid = grid + "\n"
            
        print("Score:", score[0], flush=True)
        print(grid, flush=True)
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
                
            if gridLayout[ snake[0][0] ][ snake[0][1] ] == snakeTailSymbol: #end game when snake head meets snake tail
                runGame[0] = 1

            if snake[0][0] < 0 or snake[0][1] < 0: #prevent snake from going negative
                runGame[0] = 1

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
        x = random.randint(0, len(gridLayout)-1)
        y = random.randint(0, len(gridLayout[0])-1)

        try:
            gridLayout[x][y] = fruitSymbol
        except:
            print("BAD RANDOM:", x,y, flush=True)
            print("BAD RANDOM2:", len(gridLayout)-1,len(gridLayout[0])-1, flush=True)
            pass

        time.sleep(fruitSpawnTime)
    return

#Threads END------------------------------------------------------------





        
#Functions--------------------------------------------------------------
def change(key):
    if direction[0] == 0 and key == 1:
        pass
    elif direction[0] == 1 and key == 0:
        pass
    elif direction[0] == 2 and key == 3:
        pass
    elif direction[0] == 3 and key == 2:
        pass
    else:
        direction[0] = key

def snakeDraw():
    for i in range( len(snake)-1 ): #-1 maybe error?
        if i == 0:
            gridLayout[snake[i][0]][snake[i][1]] = snakeHeadSymbol #head
        else:
            gridLayout[snake[i][0]][snake[i][1]] = snakeTailSymbol #tail

def main():
    for i in range(0, 20): #y
        gridLayout.append([])
        for p in range(0,40): #X
            gridLayout[i].append(gridSymbol)
    
    thread1 = Timer( refresh, refreshCycle )#repeatedly prints arena
    thread1.start()

    thread2 = Timer( refresh*5, snakeMovement )#moves snake around arena
    thread2.start()

    thread3 = Timer( refresh*10, fruit )
    thread3.start()


    keyboard.add_hotkey( "up", lambda: change(0) )
    keyboard.add_hotkey( "down", lambda: change(1) )
    keyboard.add_hotkey( "left", lambda: change(2) )
    keyboard.add_hotkey( "right", lambda: change(3) )
#Functions END-----------------------------------------------------------

main()
