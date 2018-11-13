'''
🐍🐍🐍 Snake: CLI ASCII Edition 🐍🐍🐍
Author: Faraz Malik
Date Created: 10/25/2018
Last Updated: 10/29/2018
'''
try: #Make sure user ran setup.bat so program will have readchar
    import readchar
except:
    raise Exception("Please run setup to install required modules")
import time, threading, random, json
from gameComponents import *

#Settings
config = {
    "fps": 4,
    "board": {
        "width": 20,
        "height": 20
    }
}

#Setup keystroke detection
keystate = {
    "UP": False,
    "DOWN": False,
    "LEFT": False,
    "RIGHT": True, #Snake will initailly be going right
    "ENTER": False, #Used for debugging
    "STATE": "RIGHT"
}

def keydowndetect(): #Thread that updates keystate
    global keystate, terminateKeylogger
    keymapping = { #Maps characters entered to game keystate
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
            keystate[state] = True #Modifies keystate
            if state != "ENTER":
                keystate["STATE"] = state
    #print("Done")

terminateKeylogger = False
keyloggerThread = threading.Thread(target=keydowndetect)
keyloggerThread.daemon = True #Make it a daemon thread
keyloggerThread.start() #Start the keylogger thread

#Initialise global components
snake = Snake(keystate["STATE"],3)
apple = Apple(0,0,0,0).newApple(Board(config["board"]["width"],config["board"]["height"]), snake)
score = 0

#Animation Loop
def updateScreen(nextFrame=True): #nextFrame is whether to update all components to the next screen  
    global keystate, apple, config, score
    gameboard = Board(config["board"]["width"],config["board"]["height"]) #Create a new board instance; like a blank canvas

    if apple.eaten:
        score += 1
        apple = apple.newApple(gameboard, snake) #Apple gets reassigned to a new location

    apple.apply(gameboard) #Draw the apple onto the board

    snake.apply(gameboard, keystate, apple, nextFrame) #Draw the snake onto the board 
    
    print(gameboard.toString(score)) #Print out the board
        
updateScreen(False) #Draw the fisrt frame
time.sleep(2) #Wait 2 seconds for game to start

while True:
    try:
        updateScreen() #Will throw an error if game over
    except:
        print('You died. Your score is %i' % score)
        
        hs_file_r = open("hs.json", 'r') #Turns hs.json into a python dict
        hs = json.loads(hs_file_r.read())
        hs_file_r.close()

        if (hs["score"] < score):
            hs_file_w = open("hs.json", "w")
            print("You made a highscore!")
            terminateKeylogger = True #Kill the keylogger so you can type your name
            input("Press enter to continue") #Its a little buggy, so you have to press enter a few times for the logger to terminate
            hs["name"] = input("Name: ")
            hs["score"] = score
            hs_file_w.write(json.dumps(hs, separators=(',',':')))
            hs_file_w.close()
        elif hs["score"] == score:
            print("lol just one more point and you would have the highscore.")
            print("The highscore of " + str(hs["score"]) + " belongs to " + hs["name"])
        else:
            print("The highscore of " + str(hs["score"]) + " belongs to " + hs["name"])
        break #Better than sys.exit() or using global variable
        
    time.sleep(1/config["fps"]) #Wait before displaying next frame

