'''
🐍🐍🐍 Snake: CLI ASCII Edition 🐍🐍🐍
Author: Faraz Malik
Date Created: 10/25/2018
Last Updated: 10/29/2018
'''
try:  # Make sure user ran setup.bat so program will have readchar
    import readchar
except:
    raise Exception("Please run setup to install required modules")
import time
import threading
import random
import json
from gameComponents import *

#User configs
extremeMode = bool(
    input("Enter 'yes' to play extreme mode, else enter nothing "))
gameMode = "extreme" if extremeMode else "normal"

#Settings
config = {
    "fps": 4,
    "board": {
        "width": 5 if extremeMode else 20,
        "height": 5 if extremeMode else 20
    }
}

#Setup keystroke detection
keystate = {
    "UP": False,
    "DOWN": False,
    "LEFT": False,
    "RIGHT": True,  # Snake will initailly be going right
    "ENTER": False,  # Used for debugging
    "STATE": "RIGHT"
}


def keydowndetect():  # Thread that updates keystate
    global keystate, terminateKeylogger
    keymapping = {  # Maps characters entered to game keystate
        "w": "UP",
        "s": "DOWN",
        "a": "LEFT",
        "d": "RIGHT",
        " ": "ENTER"
    }

    while not terminateKeylogger:
        char = readchar.readchar().decode("utf-8")
        if char in keymapping.keys():
            keystate = {
                "UP": False,
                "DOWN": False,
                "LEFT": False,
                "RIGHT": False,
                "ENTER": False,
                "STATE": None
            }
            state = keymapping[char]
            keystate[state] = True  # Modifies keystate
            if state != "ENTER":
                keystate["STATE"] = state
    #print("Done")


terminateKeylogger = False
keyloggerThread = threading.Thread(target=keydowndetect)
keyloggerThread.daemon = True  # Make it a daemon thread
keyloggerThread.start()  # Start the keylogger thread

#Initialise global components
snake = Snake(keystate["STATE"], 3, round(
    config["board"]["width"]/2), round(config["board"]["height"]/2))
apple = Apple(0, 0, 0, 0).newApple(
    Board(config["board"]["width"], config["board"]["height"]), snake)
score = 0

#Animation Loop


# nextFrame is whether to update all components to the next screen
def updateScreen(nextFrame=True):
    global keystate, apple, config, score
    # Create a new board instance; like a blank canvas
    gameboard = Board(config["board"]["width"], config["board"]["height"])

    if apple.eaten:
        score += 1
        # Apple gets reassigned to a new location
        apple = apple.newApple(gameboard, snake)

    apple.apply(gameboard)  # Draw the apple onto the board

    # Draw the snake onto the board
    snake.apply(gameboard, keystate, apple, nextFrame)

    print(gameboard.toString(score))  # Print out the board


updateScreen(False)  # Draw the fisrt frame
time.sleep(2)  # Wait 2 seconds for game to start

while True:
    try:
        updateScreen()  # Will throw an error if game over
    except:
        print('You died. Your score is %i' % score)

        hs_file_r = open("hs.json", 'r')  # Turns hs.json into a python dict
        hs = json.loads(hs_file_r.read())
        hs_file_r.close()

        if (hs[gameMode]["score"] < score):
            hs_file_w = open("hs.json", "w")
            print("You made a highscore!")
            terminateKeylogger = True  # Kill the keylogger so you can type your name
            # Its a little buggy, so you have to press enter a few times for the logger to terminate
            input("Press enter to continue")
            hs[gameMode]["name"] = input("Name: ")
            hs[gameMode]["score"] = score
            hs_file_w.write(json.dumps(hs, separators=(',', ':')))
            hs_file_w.close()
        elif hs[gameMode]["score"] == score:
            print("lol just one more point and you would have the highscore.")
            print("The highscore of " +
                  str(hs[gameMode]["score"]) + " belongs to " + hs[gameMode]["name"])
        else:
            print("The highscore of " +
                  str(hs[gameMode]["score"]) + " belongs to " + hs[gameMode]["name"])
        break  # Better than sys.exit() or using global variable

    time.sleep(1/config["fps"])  # Wait before displaying next frame
