import keyboard

thing = "asdf"
direction = [0]

def change(num):
    direction[0] = num

keyboard.add_hotkey( "right", lambda: change(55) )
keyboard.add_hotkey( "left", lambda: print(direction[0]) )
