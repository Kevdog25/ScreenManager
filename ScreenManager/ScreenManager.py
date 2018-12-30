import time
import gevent
from gevent import monkey; monkey.patch_all()
from ScreenManager.KeyListener import KeyListener, ControlKeys
from ScreenManager.Event import Event, KeyDown
from ScreenManager.Window import getScreenSize
from ScreenManager import Box
import curses

class ScreenManager:
    def __init__(self, refreshRate = 60):
        self.Running = False
        self.RootBox = Box(0, 0, *getScreenSize())
        self.RefreshRate = refreshRate
        self.debugLog = open('debugLog.txt', 'a+')
        self.Screen = None
        
    def __del__(self):
        self.debugLog.close()
    def addBox(self, box):
        self.RootBox.addChild(box)
        
    def writeBlock(self, x, y, lines):
        for i, line in enumerate(lines):
            self.Screen.addstr(y + i, x, line)
            
    def renderText(self, textArray):
        for r in textArray:
            for i, c in enumerate(r):
                if c is None:
                    r[i] = ' '
        self.writeBlock(0, 0, [''.join(r) + ' ' for r in textArray])

    def drawLoop(self):
        while self.Running:
            if self.RootBox.IsDirty():
                self.renderText(self.RootBox.render())
                self.Screen.refresh()
            gevent.sleep(1.0 / self.RefreshRate)

    def raiseKeyDown(self, char, control):
        if control in (ControlKeys.Escape, ControlKeys.Cancel):
            self.Running = False
        event = KeyDown(char, control)
        self.RootBox.onEvent(event)

    def inputLoop(self):
        with KeyListener() as listener:
            while self.Running:
                x = listener.poll()
                if x is not None:
                    self.raiseKeyDown(*x)
                gevent.sleep(0.01)

    def run(self):
        self.Screen = curses.initscr()
        self.Screen.clear()
        self.Screen.refresh()
        self.Running = True
        self.RootBox.focus()
        drawlet = gevent.spawn(self.drawLoop)
        inputlet = gevent.spawn(self.inputLoop)
        gevent.joinall([drawlet, inputlet])
        
