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

    def hitsVerticalWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x

    def hitsHorizontalWall(self, point):
        return round(point[1]) < 0 or round(point[1]) >= self._y

    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))
            
class CanvasAxes(Canvas):
    def setAxes(self):
        x = [str(i) if i % 5 == 0 else ' ' for i in range(self._x + 1)]
        y = [str(i) if i % 5 == 0 else ' ' for i in range(self._y + 1)[::-1]]
        return x, y
       
    def print(self):
        self.clear()
        for y in range(self._y):
            print(self.setAxes()[1][y] + ' ' + ' '.join([col[y] for col in self._canvas]))
        print(' '.join(self.setAxes()[0]))

class MultiScribeCanvas(Canvas):
    def initScribes(self,scribes):
        self.scribes = scribes
        for s in self.scribes:
            s['scribe'] = TerminalScribe(self)
            s['scribe'].setPosition(s['pos'])
            s['scribe'].setDirection(s['instr'][0]['dir'])
            for instr in s['instr']:
                s['scribe'].instructions.append(instr)

    def runScribes(self):
        maxInstructionLength = max([sum([instr['count'] for instr in scribInstr['instr']]) for scribInstr in self.scribes])
        for i in range(maxInstructionLength):
            for s in self.scribes:
                s['scribe'].next()

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
        self.pos = pos

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

class SquareScribe(TerminalScribe):
    def forward(self,distance):
        for i in range(distance):
            pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            if not self.canvas.hitsWall(pos):
                self.draw(pos)

    def up(self,distance=1):
        self.direction = [0, -1]
        self.forward(distance)

    def down(self,distance=1):
        self.direction = [0, 1]
        self.forward(distance)

    def right(self,distance=1):
        self.direction = [1, 0]
        self.forward(distance)

    def left(self,distance=1):
        self.direction = [-1, 0]
        self.forward(distance)

    def drawSquare(self, size):
        self.right(size)
        self.down(size)
        self.left(size)
        self.up(size)

class PlotterScribe(TerminalScribe):
    def plot(self, func):
        for x in range(self.canvas._x):
            pos = [x, func(x)+(self.canvas._y // 2)]
            if not self.canvas.hitsWall(pos):
                self.draw(pos)


scribes = [{
                'pos':  [0, 0],
                'instr':[   
                            {'dir':315,'count':3},
                            {'dir':135,'count':5},
                            {'dir':180,'count':20},
                            {'dir':270,'count':50},
                        ],
            },
            {
                'pos':  [15, 15],
                'instr': [
                            {'dir':90,'count':3},
                            {'dir':0,'count':5},
                            {'dir':270,'count':10},
                            {'dir':90,'count':30},
                        ],
            },
            {
                'pos': [0, 0],
                'instr': [
                            {'dir':135,'count':100},
                        ],
            },
            ]
canvas = MultiScribeCanvas(30, 30)
canvas.initScribes(scribes)
canvas.runScribes()
input()


def sine(x_val):
    return 5 * math.sin(x_val / 4)

def cosine(x_val):
    return 5 * math.cos(x_val / 4)

canvasAxes = CanvasAxes(30,30)
scribe = PlotterScribe(canvasAxes)
scribe.plot(sine)
scribe.plot(cosine)
input()


scribe = SquareScribe(canvas)
scribe.drawSquare(20)
scribe.right(25)
scribe.down(5)
scribe.left(30)
input("Program complete!")