from terminalscribe.terminalscribe import TerminalScribe
from terminalscribe.util import InputException

class PlotterScribe(TerminalScribe):
    def plot(self, func):
        for x in range(self.canvas._x):
            try:
                pos = [x, self.canvas._y - func(x)]
            except Exception as e:
                raise InputException(f'An error occurred. Is it possible you didn\'t pass a function that accepts an x parameter and spits out a y value?\nException: {e}')
            if not self.canvas.hitsWall(pos):
                self.draw(pos)