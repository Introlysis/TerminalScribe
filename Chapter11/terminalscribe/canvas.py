import os
import json
from terminalscribe.util import InputException, OutsideOfCanvasException, TerminalException

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

    def toDict(self):
        return {'name':type(self).__name__,'width':self._x,'height':self._y}

    @staticmethod
    def fromDict(dict):
        if not ('name' in dict and 'width' in dict and 'height' in dict):
            raise InputException('Could not find \'name\', \'width\' and \'height\' in file')
        canvas = Canvas(dict['width'],dict['height'])
        return canvas

    @staticmethod
    def loadFromFile(filename):
        with open(filename + '.json','r') as f:
            text = f.readline()
        try:
            return Canvas.fromDict(json.loads(text))
        except Exception:
            raise TerminalException(f'Could not parse JSON from file {filename + ".json"}')

    def pushToFile(self, filename):
        with open(filename + '.json','w') as f:
            f.write(json.dumps(self.toDict()))