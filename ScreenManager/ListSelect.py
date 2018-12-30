from ScreenManager import BoundedBox, TextBox
import random
from ScreenManager.KeyListener import ControlKeys

class ListSelect(BoundedBox):
    def __init__(self, options, *args, **kwargs):
        BoundedBox.__init__(self, *args, **kwargs)
        self.options = options
        self.Display = TextBox(parent = self, x = self.X + 1, y = self.Y + 1, editable = False, width = self.Width - 2, height = self.Height - 5, boundary = False)
        self.Select = TextBox(parent = self, x = self.X + 1, y = self.Y + self.Height - 4, width = self.Width - 2, height = 3)
        self.Select.onTextChange(self.updateDisplay)
        self.Select.canFocus = False
        self._events.update({
            'onSelect' : []
        })
        self.selected = None
        self.updateDisplay('')
        
    def onSelect(self, func):
        self._events['onSelect'].append(func)
    def raiseOnSelect(self):
        for f in self._events['onSelect']:
            f(self.selected)

    def updateDisplay(self, text):
        sortedOptions = sorted(((self.stringDistance(text, o), o) for o in self.options), reverse = True)
        self.options = list(v[1] for v in sortedOptions)
        if len(self.options) > 0: self.selected = self.options[0]
        w = self.Width - 2
        self.Display.InnerText = ''.join(o[:w - 1].ljust(w, ' ') for o in self.options)
        self.dirty()
    
    def onKeyDown(self, event):
        if event.Control == ControlKeys.Enter:
            self.raiseOnSelect()
        self.Select.onKeyDown(event)
        return True
    
    @staticmethod
    def stringDistance(string1, string2):
        # TODO - Implement this
        return random.randint(1,20)