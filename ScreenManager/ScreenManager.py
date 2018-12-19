import time
import gevent
from gevent import monkey; monkey.patch_all()
import msvcrt


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
        while self.Running:
            x = msvcrt.kbhit()
            self.CurrentScreen.handleInput(x)
            gevent.sleep(1.0 / self.RefreshRate)


    def run(self):
        if self.CurrentScreen is None:
            raise RuntimeError('No current screen is set. Cannot run')
        self.Running = True
        drawlet = gevent.spawn(self.drawLoop)
        inputlet = gevent.spawn(self.inputLoop)
        gevent.joinall([drawlet, inputlet])
            
