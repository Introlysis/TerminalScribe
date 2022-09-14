import threading
import time
import os
import json
from terminalscribe.util import InputException, TerminalException
from terminalscribe.canvas import Canvas
from terminalscribe.multiterminalscribe import MultiTerminalScribe

class MultiScribeCanvas(Canvas):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.framerate = 0.01
        self.threads = []

    def setFramerate(self, framerate):
        try:
            float(framerate)
        except Exception:
            raise InputException('framerate needs to be a number')
        self.framerate = float(framerate)

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

    def toDict(self):
        dict = super().toDict()
        dict['scribes'] = self.scribes.copy()
        for s in dict['scribes']:
            s['scribe'] = type(s['scribe']).__name__
        dict['framerate'] = self.framerate
        return dict

    @staticmethod
    def fromDict(dict):
        if not ('name' in dict and 'width' in dict and 'height' in dict and 'scribes' in dict and 'framerate' in dict):
            raise InputException('Could not find \'name\', \'width\', \'height\', \'scribes\' and \'framerate\' in file')
        canvas = MultiScribeCanvas(dict['width'],dict['height'])
        canvas.initScribes(dict['scribes'])
        canvas.setFramerate(dict['framerate'])
        return canvas

    @staticmethod
    def loadFromFile(filename):
        with open(filename + '.json','r') as f:
            text = f.readline()
        try:
            return MultiScribeCanvas.fromDict(json.loads(text))    
        except Exception:
            raise TerminalException(f'Could not parse JSON from file {filename + ".json"}')
