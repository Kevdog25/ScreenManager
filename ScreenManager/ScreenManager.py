import time
import gevent
from gevent import monkey; monkey.patch_all()
from ScreenManager.KeyListener import KeyListener
from ctypes import windll, create_string_buffer

class ScreenManager:
    def __init__(self, refreshRate = 60):
        self.Running = False
        self.RootBox = None
        self.RefreshRate = refreshRate
        self.Focused = None

    def setRoot(self, box):
        self.RootBox = box
        self.Focused = box

    def renderText(self, textArray):
        for r in textArray:
            for i, c in enumerate(r):
                if c is None:
                    r[i] = ' '
        rendered = '\n' + '\n'.join(''.join(r) for r in textArray)
        print(rendered, end = '')

    def drawLoop(self):
        while self.Running:
            if self.RootBox.IsDirty():
                self.RootBox.update()
                self.renderText(self.RootBox.draw())
            gevent.sleep(1.0 / self.RefreshRate)

    def inputLoop(self):
        with KeyListener() as listener:
            while self.Running:
                x = listener.poll()
                if x is not None:
                    if x == '\t':
                        nextFocus = self.Focused.nextFocus()
                        if nextFocus is None:
                            nextFocus = self.RootBox
                    elif self.Focused is not None:
                        self.Focused.handleInput(x)
                gevent.sleep(0.01)

    def run(self):
        if self.RootBox is None:
            raise RuntimeError('No current screen is set. Cannot run')
        self.Running = True
        drawlet = gevent.spawn(self.drawLoop)
        inputlet = gevent.spawn(self.inputLoop)
        gevent.joinall([drawlet, inputlet])

    @staticmethod
    def getScreenSize():
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            import struct
            (bufx, bufy, curx, cury, wattr,
            left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left
            sizey = bottom - top
        else:
            sizex, sizey = 80, 25 # Defaults

        return sizex, sizey
            
