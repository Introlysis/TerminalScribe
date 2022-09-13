import os
import time
import math
import threading
from termcolor import colored

class TerminalException(Exception):
    def __init__(self, message=''):
        super().__init__(colored(message,'red'))

class OutsideOfCanvasException(TerminalException):
    pass

class InputException(TerminalException):
    pass

def isNumber(x):
    try:
        float(x)
        return True
    except Exception:
        return False

class Canvas:
    def __init__(self, width, height):
        try:
            int(width)
            int(height)
        except Exception:
            raise InputException('Please enter whole numbers for canvas width and height')
        
        self._x = int(width)
        self._y = int(height)

        if not (self._x > 0 and self._y > 0):
            raise InputException('Please enter canvas dimensions greater than 0')

        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x or round(point[1]) < 0 or round(point[1]) >= self._y

    def hitsVerticalWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x

    def hitsHorizontalWall(self, point):
        return round(point[1]) < 0 or round(point[1]) >= self._y

    def setPos(self, pos, mark):
        try:
            self._canvas[round(pos[0])][round(pos[1])] = mark
        except Exception:
            raise OutsideOfCanvasException(f'position {pos} is outside of canvas with dimensions [{self._x}, {self._y}]')

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
    def __init__(self, width, height):
        super().__init__(width, height)
        self.framerate = 0.05
        self.threads = []

    def initScribes(self,scribes):
        for scribe in scribes:
            for instr in scribe['instr']:
                if not ('dir' in instr and 'count' in instr):
                    raise InputException('Your scribe instructions must include a \'dir\' and a \'count\'')
        
        self.scribes = scribes
        for s in self.scribes:
            s['scribe'] = MultiTerminalScribe(self)
            s['scribe'].setPosition(s['pos'])
            s['scribe'].setDirection(s['instr'][0]['dir'])
            for instr in s['instr']:
                s['scribe'].instructions.append(instr)

    def runScribes(self):
        maxInstructionLength = max([sum([instr['count'] for instr in scribInstr['instr']]) for scribInstr in self.scribes])
        for i in range(maxInstructionLength):
            self.threads = []
            for s in self.scribes:
                self.threads.append(threading.Thread(target=s['scribe'].next))
            [t.start() for t in self.threads]
            [t.join() for t in self.threads]
            self.print()
            time.sleep(self.framerate)

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

class MultiTerminalScribe(TerminalScribe):
    def forward(self):
        if self.instructions[self.instrTracker]['count'] == 0:
            return 0
        nextPos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        self.direction[0] = -self.direction[0] if self.canvas.hitsVerticalWall(nextPos) else self.direction[0]
        self.direction[1] = -self.direction[1] if self.canvas.hitsHorizontalWall(nextPos) else self.direction[1]
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.instructions[self.instrTracker]['count'] -= 1

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
            try:
                pos = [x, self.canvas._y - func(x)]
            except Exception as e:
                raise InputException(f'An error occurred. Is it possible you didn\'t pass a function that accepts an x parameter and spits out a y value?\nException: {e}')
            if not self.canvas.hitsWall(pos):
                self.draw(pos)


scribes = [{
                'pos':  ['0', 0],
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
                            {'dir':180,'count':5},
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

"""
def sine(x_val):
    return 5 * math.sin(x_val / 4) + 15

def cosine(x_val):
    return 5 * math.cos(x_val / 4) + 15

def errorFunc(x_val):
    return(x_val * 2)

canvasAxes = CanvasAxes(30,30)
scribe = PlotterScribe(canvasAxes)
scribe.plot(sine)
scribe.plot(cosine)
scribe.plot(errorFunc)
input("Done!")
"""
"""
canvas = Canvas(30,30)
scribe = SquareScribe(canvas)
scribe.drawSquare(20)
scribe.right(25)
scribe.down(5)
scribe.left(30)
input("Program complete!")
"""