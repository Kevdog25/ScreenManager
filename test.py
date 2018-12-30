from ScreenManager import Box, ScreenManager
from ScreenManager import BoundedBox, TextBox
from ScreenManager import ListSelect
from ScreenManager.Window import getScreenSize
from ScreenManager import ModalWindow
import gevent


def printString(string):
    print(string)
    
    
def raiseWindow(box2, options):
    ModalWindow.RaiseListSelect(box2, options, printString)
    

if __name__ == '__main__':
    options = ['hello', 'this is a longer one. I hope it works']
    manager = ScreenManager()
    box1 = BoundedBox(0, 0, 10, 10)
    box2 = TextBox(x = 10, y = 10, width = 20, height = 10)
    #box2 = ListSelect(options, x = 10, y = 10, width = 20, height = 10)
    manager.addBox(box1)
    manager.addBox(box2)
    gevent.spawn_later(1, raiseWindow, box2, options)
    manager.setRoot(root)
    manager.run()