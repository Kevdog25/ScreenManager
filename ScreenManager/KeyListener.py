from win32api import STD_INPUT_HANDLE
from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT


class KeyListener:
    def __enter__(self):
        self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
        self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

        self.curEventLength = 0
        self.curKeysLength = 0

        self.capturedChars = []

        return self

    def __exit__(self, type, value, traceback):
        pass

    def poll(self):
        if not len(self.capturedChars) == 0:
            return self.capturedChars.pop(0)

        eventsPeek = self.readHandle.PeekConsoleInput(10000)

        if len(eventsPeek) == 0:
            return None

        if not len(eventsPeek) == self.curEventLength:
            for curEvent in eventsPeek[self.curEventLength:]:
                if curEvent.EventType == KEY_EVENT:
                    if ord(curEvent.Char) == 0 or not curEvent.KeyDown:
                        pass
                    else:
                        curChar = str(curEvent.Char)
                        self.capturedChars.append(curChar)
            self.curEventLength = len(eventsPeek)

        if not len(self.capturedChars) == 0:
            return self.capturedChars.pop(0)
        else:
            return None