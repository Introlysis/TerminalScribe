from terminalscribe.terminalscribe import TerminalScribe

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
