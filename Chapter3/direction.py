from terminalscribe import TerminalScribe
from canvas import Canvas

scribe = TerminalScribe(Canvas(250,250),200)
for i in range(10):
    scribe.forward()