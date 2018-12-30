from ScreenManager.Event import Event, KeyDown
from copy import deepcopy

class Box:
    def __init__(self, x, y, width, height, parent = None):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.Parent = parent
        if self.Parent is not None:
            self.Parent.addChild(self)
        self.Buffer = [[' ' for w in range(self.Width)] for h in range(self.Height)]
        self.Children = []
        self.Focus = False
        self._focus = False
        self.canFocus = True
        self._events = {}
        self.dirty()
    
    def removeChild(self, box):
        i = self.Children.index(box)
        del self.Children[i]
        self.dirty()
    
    def addChild(self, box):
        self.Children.append(box)
        box.Parent = self
        
    def getRoot(self):
        if self.Parent is None:
            return self
        return self.Parent.getRoot()

    def render(self):
        # TODO - This is hella slow. Just rerender everything all the time.
        rendered = deepcopy(self.Buffer)
        for box in self.Children:
            boxText = box.render()
            relY, relX = box.Y - self.Y, box.X - self.X
            for y, row in enumerate(boxText):
                if y + relY >= self.Height or y + relY < 0:
                    continue
                for x, cell in enumerate(row):
                    if cell is None:
                        continue
                    if x + relX >= self.Width or x + relX < 0:
                        continue
                    rendered[y + relY][x + relX] = cell
        self._dirty = False
        self.Dirty = False
        return rendered

    def IsDirty(self):
        return self.Dirty
    
    def dirty(self):
        self.Dirty = True
        self._dirty = True
        parent = self.Parent
        while parent is not None and not parent.Dirty:
            parent.Dirty = True
            parent = parent.Parent
        
    # Events
    def onEvent(self, event):
        if self._focus:
            if isinstance(event, KeyDown):
                if self.onKeyDown(event):
                    if event.Char == '\t':
                        self.nextFocus()
        else:
            for child in self.Children:
                if child.Focus:
                    child.onEvent(event)
                    break
        return

    # Overridable events
    def onKeyDown(self, event):
        '''You can override this. Return True if you want the event to propogate.
            Return False if you don\'t want default handling'''
        return True

    def onFocus(self):
        '''Default is to pass focus to children in order'''
        for c in self.Children:
            if c.canFocus:
                c.focus()
                break
        return

    def onLoseFocus(self):
        pass
        
        
    # Sketchy Focus stuff down here.
    def focus(self):
        self._focus = True
        parents = self.getPathToFocus()
        if not parents:
            self._focus = True
            self.Focus = True
            self.onFocus()
            return True
        
        parents[0]._focus = False
        parents[0].removeFocusFromChildren()

        for p in parents[1:]:
            p.Focus = True
        self.Focus = True
        self.onFocus()
        return True

    def removeFocus(self):
        self.Focus = False
        self._focus = False
        self.onLoseFocus()
        self.removeFocusFromChildren()
        return

    def removeFocusFromChildren(self):
        for child in self.Children:
            if child.Focus:
                child.removeFocus()
                break
        return

    def getPathToFocus(self):
        parent = self.Parent
        l = []
        while parent is not None and not parent.Focus:
            l.append(parent)
            parent = parent.Parent
        if parent is not None:
            l.append(parent)
        return list(reversed(l))
        

    def cycleFocus(self, child):
        nextIndex = self.Children.index(child) + 1
        for child in self.Children[nextIndex:]:
            if child.canFocus:
                child.focus()
                return

        if self.Parent is not None:
            self.Parent.cycleFocus(self)
            return
        self.focus()

        return
        
    def nextFocus(self):
        for child in self.Children:
            if child.canFocus:
                child.focus()
                return
        if self.Parent is not None:
            self.Parent.cycleFocus(self)
        return

    
        
        