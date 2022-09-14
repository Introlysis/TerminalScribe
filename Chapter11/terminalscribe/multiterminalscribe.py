from terminalscribe.terminalscribe import TerminalScribe
from termcolor import colored

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