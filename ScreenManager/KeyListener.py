from win32api import STD_INPUT_HANDLE
from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT
from enum import IntEnum


class ControlKeys(IntEnum):
    Enter = 13
    Shift = 16
    Control = 17
    Alt = 18
    Cancel = 24
    Escape = 27
    Left = 37
    Up = 38
    Right = 39
    Down = 40

controlKeyValues = set(map(int, ControlKeys))

class KeyListener:
    def __enter__(self):
        self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
        self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

        self.capturedChars = []

        return self

    def __exit__(self, type, value, traceback):
        pass

    def poll(self):
        if self.capturedChars:
            return self.capturedChars.pop(0)

        eventsPeek = self.readHandle.PeekConsoleInput(10000)

        if len(eventsPeek) == 0:
            return None

        eventsPeek = self.readHandle.ReadConsoleInput(10000)

        for curEvent in eventsPeek:
            if curEvent.EventType == KEY_EVENT:
                if not curEvent.KeyDown:
                    pass
                else:
                    char, control = None, None
                    if curEvent.VirtualKeyCode in controlKeyValues:
                        control = ControlKeys(curEvent.VirtualKeyCode)
                    else:
                        char = curEvent.Char
                    self.capturedChars.append((char, control))

        if self.capturedChars:
            return self.capturedChars.pop(0)
        else:
            return None