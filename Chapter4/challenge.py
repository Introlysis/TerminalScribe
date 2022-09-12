import os
import time
import math
from termcolor import colored

class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x or round(point[1]) < 0 or round(point[1]) >= self._y

    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.1
        self.pos = [0, 0]
        self.direction = [0, 0]
        self.instructions = []
        self.instrTracker = {'action' : 0, 'iter' : 1}
        self.done = False

    def setDirection(self, deg):
        radians = (deg/180) * math.pi
        self.direction = [math.sin(radians), -math.cos(radians)] #negative cosine because up is negative
        
    def setPosition(self, pos):
        self.pos = pos
        
    def next(self):
        if self.done:
            return
        if self.instrTracker['iter'] > self.instructions[self.instrTracker['action']]['count']:
            self.instrTracker['action'] += 1
            if self.instrTracker['action'] >= len(self.instructions):
                self.done = True
                return
        self.setDirection(self.instructions[self.instrTracker['action']]['dir'])
        self.forward()
        self.instrTracker['iter'] += 1
        
    def forward(self):
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)
        
    def up(self):
        self.direction = [0, -1]
        self.forward()

    def down(self):
        self.direction = [0, 1]
        self.forward()

    def right(self):
        self.direction = [1, 0]
        self.forward()

    def left(self):
        self.direction = [-1, 0]
        self.forward()

    def drawSquare(self, size):
        i = 0
        while i < size:
            self.right()
            i = i + 1
        i = 0
        while i < size:
            self.down()
            i = i + 1
        i = 0
        while i < size:
            self.left()
            i = i + 1
        i = 0
        while i < size:
            self.up()
            i = i + 1



    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)

canvas = Canvas(30, 30)
scribes = [{
                'pos':  [0, 0],
                'instr':[   
                            {'dir':135,'count':5},
                            {'dir':180,'count':20},
                        ],
            },
            {
                'pos':  [15, 15],
                'instr': [
                            {'dir':90,'count':3},
                            {'dir':0,'count':5},
                            {'dir':270,'count':10},
                        ],
            }]

def runScribes(scribes):
    for s in scribes:
        s['scribe'] = TerminalScribe(canvas)
        s['scribe'].setPosition(s['pos'])
        for instr in s['instr']:
            s['scribe'].instructions.append(instr)
    maxInstructionLength = max([sum([instr['count'] for instr in scribInstr['instr']]) for scribInstr in scribes])
    for i in range(maxInstructionLength):
        for s in scribes:
            s['scribe'].next()
        
runScribes(scribes)

"""scribe = TerminalScribe(canvas)
scribe.drawSquare(20)
scribe.setDirection(135)
for i in range(30):
    scribe.forward()    
scribe.setDirection(50)
for i in range(15):
    scribe.forward()"""
