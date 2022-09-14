from terminalscribe.canvas import Canvas

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