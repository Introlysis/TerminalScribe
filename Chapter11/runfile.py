import json
from argparse import ArgumentParser
from terminalscribe.util import InputException
from terminalscribe.multiscribecanvas import MultiScribeCanvas

parse = ArgumentParser()
parse.add_argument('--file', '-f',required=True,help='.json file from which to read TerminalScribe data')
args = parse.parse_args()

try:
    with open(args.file, 'r') as f:
        results = json.loads(f.readline())
except Exception as e:
    raise InputException(f'Could not parse JSON from {args.file}\n{e}')

if not 'name' in results:
    raise InputException('No \'name\' found in file')
if results['name'] == 'MultiScribeCanvas':
    canvas = MultiScribeCanvas.fromDict(results)
    canvas.runScribes()
else:
    raise InputException('Could not determine what object to create')




"""
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
"""
"""
scribes = [{"pos": [10, 5],"instr": [{"dir": 270, "count": 5},{"dir": 90, "count": 10}],"scribe": "MultiTerminalScribe"},{"pos": [10, 5],"instr": [{"dir": 180, "count": 10},{"dir": 225, "count": 2},{"dir": 270, "count": 2},{"dir": 315, "count": 2}],"scribe": "MultiTerminalScribe"},{"pos": [15, 11],"instr": [{"dir": 90, "count": 1},{"dir": 135, "count": 2},{"dir": 180, "count": 2},{"dir": 225, "count": 2},{"dir": 270, "count": 2},{"dir": 315, "count": 2},{"dir": 0, "count": 2},{"dir": 45, "count": 2},{"dir": 90, "count": 1}],"scribe": "MultiTerminalScribe"},{"pos": [20, 14],"instr": [{"dir": 90, "count": 4},{"dir": 45, "count": 2},{"dir": 315, "count": 2},{"dir": 270, "count": 4},{"dir": 225, "count": 2},{"dir": 180, "count": 2},{"dir": 135, "count": 2},{"dir": 90, "count": 4}],"scribe": "MultiTerminalScribe"}]
canvas = MultiScribeCanvas(30, 30)
canvas.initScribes(scribes)
canvas.pushToFile('test_file')
canvas2 = MultiScribeCanvas.loadFromFile('test_file')
canvas2.runScribes()
input()
"""
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