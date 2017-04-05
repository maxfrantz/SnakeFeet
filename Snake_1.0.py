#!/usr/bin/python

#ToDo
#--------
#1. Make a Snake Class
#   A. Key events will "turn" the snake
#       i. turn will be executed on subsequent "advance" triggered by timer
#   B. Timer execute "advance" method, advancing snake one unit in direction it is headed
#       i.  Advance method needs to check if snake has intersected with itself or apple
#       ii. Advnace method also needs to check if snake has left board, in which case head needs to be set to opposite side
#           a. possible game variant: head is sent to random pixel--"wormhole"
#   C. When head intersects apple, call "grow" method
#   D. Add "occupied" set to board where snake's coords are occupied
#   E. Add
#2. Apple randomly populated on board

from tkinter import *
import time
import random

random.seed()

class Snake(Canvas):
    bgColor    = "black"
    bodyColor = "#adadad" #grey
    headColor = "yellow"
    appleColor = "red"
    active = True
    advanceType = "full"
    gameTag = "gameTag"

    def __init__(self,master,pixelSize,boardHeight,boardWidth,headStartX,headStartY,snakeLength,heading,updateLength):
        #dimensions are in pixels of size board.pixelSize
        #startHeading is the initial heading of the Snake
        #master is a Tk() object

        self.master = master
        self.pixelSize = pixelSize
        self.boardHeight = boardHeight
        self.boardWidth = boardWidth
        self.canvasHeight = boardHeight*pixelSize
        self.canvasWidth = boardWidth*pixelSize
        self.headX = headStartX
        self.headY = headStartY
        self.length = snakeLength
        self.heading = heading
        self.updateLength = updateLength

        Canvas.__init__(self, master=master, bg=self.bgColor,
                        height=self.canvasHeight, width=self.canvasWidth)
       
        self.snakeHeadCoord = (self.pixelSize*self.headX,
                                self.pixelSize*self.headY,
                                self.pixelSize*(self.headX-1),
                                self.pixelSize*self.headY-self.pixelSize)
        self.snakeBodyCoord = [(self.pixelSize*x,
                                self.pixelSize*self.headY,
                                self.pixelSize*(x-1),
                                self.pixelSize*self.headY-self.pixelSize) for x in range(1,self.length+1)]

        self.snakeHead = self.create_rectangle(
            self.snakeHeadCoord, fill=self.headColor, width=0, tag=self.gameTag)
        self.snakeBody = [self.create_rectangle(
            self.snakeBodyCoord[x],fill=self.bodyColor, width=0, tag=self.gameTag) for x in range(len(self.snakeBodyCoord))]

        self.appleXY = [random.randint(0,self.boardWidth),random.randint(0,self.boardHeight)]
        self.appleCoord = (self.pixelSize*self.appleXY[0],
                           self.pixelSize*self.appleXY[1],
                           self.pixelSize*(self.appleXY[0]-1),
                           self.pixelSize*(self.appleXY[1]-1))
        self.apple = self.create_rectangle(
            self.appleCoord, fill=self.appleColor, width=0, tag=self.gameTag)
        
        self.pack()
        
    def advance(self,advanceType):
        if self.heading == "L":
            self.headX -= 1
            if self.headX < 0:
                self.headX = self.boardWidth
        elif self.heading == "R":
            self.headX += 1
            if self.headX > self.boardWidth:
                self.headX = 0
        elif self.heading == "U":
            self.headY -= 1
            if self.headY < 0:
                self.headY = self.boardHeight
        elif self.heading == "D":
            self.headY += 1
            if self.headY > self.boardHeight:
                self.headY = 0

        if advanceType == "full":
            for ind in range(0,len(self.snakeBodyCoord)):
                if ind == len(self.snakeBodyCoord)-1:
                    self.snakeBodyCoord[ind] = self.snakeHeadCoord
                    self.coords(self.snakeBody[ind], self.snakeBodyCoord[ind])
                else:    
                    self.snakeBodyCoord[ind] = self.snakeBodyCoord[ind+1]
                    self.coords(self.snakeBody[ind], self.snakeBodyCoord[ind])
        elif advanceType == "grow":
            self.advanceType = "full"
            self.snakeBodyCoord.append(self.snakeHeadCoord)
            self.snakeBody.append(self.create_rectangle(
                self.snakeBodyCoord[-1],fill=self.bodyColor, width=0, tag=self.gameTag))
                                  
        self.snakeHeadCoord = (self.pixelSize*self.headX,
                                self.pixelSize*self.headY,
                                self.pixelSize*(self.headX-1),
                                self.pixelSize*self.headY-self.pixelSize)
        self.coords(self.snakeHead, self.snakeHeadCoord)
        

        if self.snakeHeadCoord in self.snakeBodyCoord:
            self.tag_raise(self.snakeHead)
            self.game_over("GAME OVER","red")

        if self.snakeHeadCoord == self.appleCoord:
            self.grow()
            self.place_apple()
        

    def key_input(self,event,direction):
        if direction == "L" and self.heading != "R":
            self.heading = "L"
        elif direction == "R" and self.heading != "L":
            self.heading = "R"
        elif direction == "U" and self.heading != "D":
            self.heading = "U"
        elif direction == "D" and self.heading != "U":
            self.heading = "D"

    def place_apple(self):
        self.appleXY = [random.randint(1,self.boardWidth),random.randint(1,self.boardHeight)]
        self.appleCoord = (self.pixelSize*self.appleXY[0],
                           self.pixelSize*self.appleXY[1],
                           self.pixelSize*(self.appleXY[0]-1),
                           self.pixelSize*(self.appleXY[1]-1))
        self.coords(self.apple, self.appleCoord)

    def grow(self):
        self.length += 1
        self.advanceType = "grow"
        
        self.updateLength -= 0.01
        if self.updateLength < 0.05:
            self.game_over("YOU WIN","green")

    def game_over(self,message,color):
        print("game over",message)
        self.active = False
        self.create_text(round(self.canvasWidth/2), round(self.canvasHeight/2),
                         fill=color, font="Times 20 bold",
                         text=message)
        self.delete(self.gameTag)

    def start(self):
        self.startTime = time.monotonic()

        while self.active:
            root.update_idletasks()
            root.update()
            if time.monotonic()>(self.startTime+self.updateLength):
                self.advance(self.advanceType)
                self.startTime = time.monotonic()

    def pause(self,event):
        if self.active:
            self.active = False
        else:
            self.active = True
            self.start()

 

#The actual game-------------     

pixelSize    = 8
boardHeight  = 30
boardWidth   = 30
headStartX   = 7
headStartY   = 12
snakeLength  = 6
heading      = "R"
updateLength = 0.2 #second

root = Tk()
root.title("Snake Feet")

game = Snake(root,pixelSize,boardHeight,boardWidth,headStartX,headStartY,snakeLength,heading,updateLength)

root.bind('<Left>', lambda event: game.key_input(event,"L"))
root.bind('<Right>', lambda event: game.key_input(event,"R"))
root.bind('<Up>', lambda event: game.key_input(event,"U"))
root.bind('<Down>', lambda event: game.key_input(event,"D"))
root.bind('<space>', game.pause)

game.start()
