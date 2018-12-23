from ScreenManager.Event import Event, KeyDown

class Box:
    def __init__(self, x, y, width, height, parent = None):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.Parent = parent
        if self.Parent is not None:
            self.Parent.addChild(self)
        self.Dirty = True
        self._dirty = True
        self.Text = [[None for w in range(self.Width)] for h in range(self.Height)]
        self.Children = []
        self.Focus = False
        self._focus = False

    def addChild(self, box):
        self.Children.append(box)
        box.Parent = self

    def update(self):
        needsUpdate = self._dirty
        if needsUpdate:
            self.Text = self.draw()
        for box in self.Children:
            needsUpdate = needsUpdate or box.IsDirty()
            if not needsUpdate:
                continue
            box.update()
            boxText = box.draw()
            for y, row in enumerate(boxText):
                if y + box.Y >= self.Height or y + box.Y < 0:
                    continue
                for x, cell in enumerate(row):
                    if cell is None:
                        continue
                    if x + box.X >= self.Width or x + box.X < 0:
                        continue
                    self.Text[y + box.Y][x + box.X] = cell
        self._dirty = False
        self.Dirty = False

    def draw(self):
        return self.Text

    def IsDirty(self):
        return self.Dirty
    
    def dirty(self):
        self.Dirty = True
        self._dirty = True
        parent = self.Parent
        while parent is not None:
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

    def canFocus(self):
        return True
        
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
            if child.canFocus():
                child.focus()
                return

        if self.Parent is not None and self.Parent.cycleFocus(self):
            return
        
        self.focus()

        return
        
    def nextFocus(self):
        for child in self.Children:
            if child.canFocus():
                child.focus()
                return
        if self.Parent is not None:
            self.Parent.cycleFocus(self)
        return

        
        