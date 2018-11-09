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
from pythonToolkit import typeinput, finish

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
    "ENTER": False,
    "STATE": "RIGHT"
}

def keydowndetect(): #Fn that updates keystate
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
keyloggerThread.start() #Start the keylooger thread

#Initialise global components
snake = Snake(keystate["STATE"],3)
apple = Apple(0,0,0,0).newApple(Board(config["board"]["width"],config["board"]["height"]),snake)
score = 0



#Animation Loop
def updateScreen(nextFrame=True): #nextFrame is whether to advance to the next frame or not
    global keystate, apple, config, score
    gameboard = Board(config["board"]["width"],config["board"]["height"]) #Create a new board instance

    if not apple.eaten:
        apple.apply(gameboard)
    else: 
        score+=1
        apple = apple.newApple(gameboard, snake)

    snake.apply(gameboard, keystate, apple, nextFrame) #Draw the snake on the board 
    
    print(gameboard.toString(score))
        
updateScreen(False)
time.sleep(2)

while True:
    try:
        updateScreen()
    except:
        print('You died. Your score is %i' % score)
        
        hs_file_r = open("hs.json", 'r') #Turns hs.json into a python dict
        hs = json.loads(hs_file_r.read())
        hs_file_r.close()

        if (hs["score"] < score):
            hs_file_w = open("hs.json", "w")
            print("You made a highscore!")
            terminateKeylogger = True
            input("Press enter to continue")
            hs["name"] = input("Name: ")
            hs["score"] = score
            hs_file_w.write(json.dumps(hs, separators=(',',':')))
            hs_file_w.close()
        else:
            print("The highscore of " + str(hs["score"]) + " belongs to " + hs["name"])
        break #Better than sys.exit() or using global variable
    time.sleep(1/config["fps"])

#finish()

