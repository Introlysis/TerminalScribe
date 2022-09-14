import math
import time
from terminalscribe.util import InputException
from termcolor import colored

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.05
        self.pos = [0, 0]
        self.direction = [0, 0]
        self.instructions = []
        self.instrTracker = 0
        self.done = False

    def setDirection(self, deg):
        radians = (deg/180) * math.pi
        self.direction = [math.sin(radians), -math.cos(radians)] #negative cosine because up is negative
        
    def setPosition(self, pos):
        try:
            [float(x) for x in pos]
        except Exception:
            raise InputException(f'Please enter a list of 2 numbers for position. You have entered {pos}')
        self.pos = [float(x) for x in pos]

    def next(self):
        if self.done:
            return
        if self.forward() == 0:
            self.instrTracker += 1
            if self.instrTracker >= len(self.instructions):
                self.done = True
                return
            self.setDirection(self.instructions[self.instrTracker]['dir'])
        
    def forward(self):
        if self.instructions[self.instrTracker]['count'] == 0:
            return 0
        nextPos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        self.direction[0] = -self.direction[0] if self.canvas.hitsVerticalWall(nextPos) else self.direction[0]
        self.direction[1] = -self.direction[1] if self.canvas.hitsHorizontalWall(nextPos) else self.direction[1]
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        self.draw(pos)
        self.instructions[self.instrTracker]['count'] -= 1

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)
