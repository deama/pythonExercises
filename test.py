from pynput import keyboard

#The key combination to check
COMBINATIONS = [
    {keyboard.Key.up},
    {keyboard.Key.down},
    {keyboard.Key.right},
    {keyboard.Key.left}
]

#The currently active modifiers
current = set()

def execute(key):
    if key == keyboard.Key.up:
        print("THING")

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute(key)

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
