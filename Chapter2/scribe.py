from c02_07_challenge import Canvas, TerminalScribe

def draw_square(side):
    canvas = Canvas(side,side)
    scribe = TerminalScribe(canvas)

    for i in range(side):
        scribe.right()
    for i in range(side):
        scribe.down()
    for i in range(side):
        scribe.left()
    for i in range(side):
        scribe.up()

draw_square(2)