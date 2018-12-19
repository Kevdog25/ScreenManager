import time
import gevent
from gevent import monkey; monkey.patch_all()
import msvcrt
from ScreenManager import KeyListener

class ScreenManager:
    def __init__(self, refreshRate = 60):
        self.Running = False
        self.CurrentScreen = None
        self.RefreshRate = refreshRate

    def setCurrent(self, screen):
        self.CurrentScreen = screen

    def drawLoop(self):
        while self.Running:
            if self.CurrentScreen.IsDirty:
                self.CurrentScreen.update()
                self.CurrentScreen.draw()
            gevent.sleep(1.0 / self.RefreshRate)

    def inputLoop(self):
        with KeyListener() as listener:
            while self.Running:
                x = listener.poll()
                if x is not None:
                    self.CurrentScreen.handleInput(x)
                gevent.sleep(0.01)

    def run(self):
        if self.CurrentScreen is None:
            raise RuntimeError('No current screen is set. Cannot run')
        self.Running = True
        drawlet = gevent.spawn(self.drawLoop)
        inputlet = gevent.spawn(self.inputLoop)
        gevent.joinall([drawlet, inputlet])
            
