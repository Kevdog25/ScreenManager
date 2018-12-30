from ScreenManager import BoundedBox
from ScreenManager.Window import getScreenSize
from ScreenManager import ListSelect

class ModalWindow(BoundedBox):
    def __init__(self, innerBox, source, callback, *args, **kwargs):
        
        BoundedBox.__init__(self, parent = source.getRoot(), *args, **kwargs)
        self.innerBox = innerBox
        self.addChild(innerBox)
        self.canFocus = False
        self.callback = callback
        self.source = source
    
    def onKeyDown(self, event):
        self.innerBox.onKeyDown(event)
        return False
        
    def close(self):
        self.Parent.removeChild(self)
        self.Parent.dirty()
        self.source.focus()
        
    def handleCallback(self, *args, **kwargs):
        self.callback(*args, **kwargs)
        self.close()
        
        
    @classmethod
    def RaiseListSelect(cls, source, options, callback):
        screenW, screenH = getScreenSize() # TODO - This is a bug. Should get the root box sizes
        width = min(max(map(len, options)) + 2, (2 * screenW) // 3)
        height = min(len(options) + 5, (2 * screenH) // 3)
        x = int(screenW / 2 - width / 2)
        y = int(screenH / 2 - height / 2)
        listSelect = ListSelect(options = options, x = x, y = y, width = width, height = height)
        modal = ModalWindow(innerBox = listSelect, source = source, callback = callback, boundary = None, x = x, y = y, width = width, height = height)
        listSelect.onSelect(modal.handleCallback)
        modal.focus()