#Board API
class Board: #Creates an empty map of pixels; like a canvas
    def __init__(self,width,height):
        m = [] #Map array
        for i in range(height):
            m.append([])
            for _ in range(width):
                m[i].append(0)
        self.board = m
        self.width = width
        self.height = height
        self.components = {}
    def togglePixel(self,x,y,char=1): #Turns specified pixel into specified charcode
        "Pixels are zero indexed"
        if x < 0 or y < 0:
            raise IndexError("Out of bounds!")
        elif x > self.width - 1 or y > self.height - 1:
            raise IndexError("Out of bounds!")
        
        self.board[y][x] = char
    def toString(self, score=0):
        "Turns board array into string"
        res = []
        board = self.board
        for row in range(self.height):
            res.append(" ".join(map(str, board[row])))
            res.append("\n")
        return "\n"+ str(score) + "\n" + "".join(res).replace("0","-").replace("1","🐍").replace("2","🍎") #Swap out charcodes for actual chars

class Component: #A box
    def __init__(self,x=0,y=0,width=1,height=1,char=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.char = char
    def apply(self,gameboard):
        gameboard.togglePixel(self.x,self.y, self.char)
class Apple(Component):
    eaten = False
    def newApple(self,gameboard, snake):
        import random
        apple = None
        appleCollision = True
        while appleCollision: #To make sure an apple does not land on the snake
            appleCollision = False
            apple = Apple(random.randint(0,gameboard.width-1),random.randint(0,gameboard.height-1),1,1,2)
            for i in range(len(snake.body)):
                if apple.x == snake.body[i].x and apple.y == snake.body[i].y:
                    appleCollision = True
        return apple
                

class Snake: #Container for conponents, with snakelike methods
    def __init__(self,direction,length=3,x=10,y=10):
        body = []
        for i in range(length):
            body.append(Component(x-i,y)) #Pastes pixels from right to left, to the front is initially the right end of the snake
        self.body = body
        self.direction = direction
    def move(self, apple):
        "The snake is moved by removing the last peice on the snake and adding a new piece to the front"
        d = self.direction
        head = self.body[0]
        x = head.x #X for peice added to the front
        y = head.y #Y for peice adde dto the front


        if d == "LEFT": #Make coordinates for new peice of the snake
            x-=1
        elif d == "RIGHT":
            x+=1
        elif d == "UP":
            y-=1
        elif d == "DOWN":
            y+=1

        if not apple.eaten and head.x == apple.x and head.y == apple.y: #You ate an apple!
            if d == "LEFT": #Undo the previous move
                x+=1
            elif d == "RIGHT":
                x-=1
            elif d == "UP":
                y+=1
            elif d == "DOWN":
                y-=1
            self.body.insert(0,Component(apple.x,apple.y,1,1))
            apple.eaten = True
        else:
            for i in range(3,len(self.body)): #Make sure snake does not bite itself
                bodypiece = self.body[i]
                if head.x == bodypiece.x and head.y == bodypiece.y: #Ya bit yerself
                    #print(i, ", len: ", len(self.body))
                    raise Exception("Bit yourself!")

            self.body.pop(-1) #Get rid of the last part of the snake
            self.body.insert(0, Component(x,y,1,1))

    def addToBody(self,comp):
        self.body.append(comp)
    def apply(self, board, keystate, apple, moveSnake=True): #Draw on board
        d = self.direction
        state = keystate["STATE"]
        
        if (d == "UP" and state == "DOWN") or (d == "DOWN" and state == "UP") or (d == "LEFT" and state == "RIGHT") or (d == "RIGHT" and state == "LEFT"):
            "The snake can only turn, not reverse"
        else:
            self.direction = state #Sync the snake's direcion with the keystate

        moveSnake and self.move(apple) #Move apple only if specified

        for i in range(len(self.body)):
            self.body[i].apply(board)
