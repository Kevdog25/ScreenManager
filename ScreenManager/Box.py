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
        self.FocusIndex = -1
    
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
        
    def handleInput(self, x):
        pass

    def afterGainFocus(self):
        return True
    def beforeLoseFocus(self):
        return True

    def nextFocus(self):
        # TODO - None of this works. Not sure what I should do with focus
        nextFocus = self.Children[self.FocusIndex].nextFocus()

        if self.FocusIndex >= len(self.Children):
            return None
        
        