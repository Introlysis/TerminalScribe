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
