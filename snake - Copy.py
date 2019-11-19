import time
from threading import Timer
from pynput import keyboard

gridLayout = [[]]
snake = [[9,8],[9,9],[9,10],[9,11]]
refresh = 0.4
gridSymbol = 0

direction = "down"




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
        direction = "up"
    elif key == keyboard.Key.down:
        direction = "down"
    elif key == keyboard.Key.left:
        direction = "left"
    elif key == keyboard.Key.right:
        direction = "right"
    print(direction)

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute(key)

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
#KEY LISTENER END-----------------------------------------------------






def refreshCycle():
    snakeDraw() #just once
    while True:
        grid = "\n"
        for i, thing in enumerate(gridLayout):
            for cell in thing:
                grid = grid + str(cell)
            grid = grid + "\n"
        print(grid)
        time.sleep(refresh) 

def snakeMovement():
    storeOld = [0,0]
    storeOld2 = [0,0]
    while True:
        print(direction)
        storeOld[0] = snake[0][0]
        storeOld[1] = snake[0][1]
        if direction == "up":
            snake[0][0] = snake[0][0] - 1
        if direction == "left":
            snake[0][1] = snake[0][1] - 1
        if direction == "right":
            snake[0][1] = snake[0][1] + 1
        if direction == "down":
            snake[0][0] = snake[0][0] + 1

        for i in range( 1, len(snake) ):
            storeOld2[0] = snake[i][0]
            storeOld2[1] = snake[i][1]
            snake[i][0] = storeOld[0]
            snake[i][1] = storeOld[1]
            storeOld[0] = storeOld2[0]
            storeOld[1] = storeOld2[1]

        snakeDraw()
                
        gridLayout[ snake[len(snake)-1][0] ][ snake[len(snake)-1][1] ] = gridSymbol
        
        time.sleep(refresh)

def snakeDraw():
    for i in range( len(snake)-1 ): #-1 maybe error?
        if i == 0:
            gridLayout[snake[i][0]][snake[i][1]] = "+" #head
        else:
            gridLayout[snake[i][0]][snake[i][1]] = "=" #tail

def main():
    for i in range(0, 20):
        gridLayout.append([])
        for p in range(0,20):
            gridLayout[i].append(gridSymbol)
    
    thread1 = Timer( refresh, refreshCycle )
    thread1.start()

    thread2 = Timer( refresh*5, snakeMovement )
    thread2.start()

    #Listen for keys
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

main()
