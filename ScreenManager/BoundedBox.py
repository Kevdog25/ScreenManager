from ScreenManager import Box
from enum import Enum, auto

class BoundaryStyle(Enum):
    Single = auto()
    Double = auto()
    Rounded = auto()

class BoundedBox(Box):
    def __init__(self, x, y, width, height, transparent = False):
        Box.__init__(self, x, y, width, height)
        self.Boundary = BoundaryStyle.Single
        char = None if transparent else ' '
        self.Text = [[char for w in range(self.Width)] for h in range(self.Height)]
        self.updateBoundary()

    def onFocus(self):
        self.Boundary = BoundaryStyle.Double
        self.updateBoundary()
        self.dirty()

    def onLoseFocus(self):
        self.Boundary = BoundaryStyle.Single
        self.updateBoundary()
        self.dirty()

    def updateBoundary(self):
        if self.Boundary is None:
            return

        if self.Width < 3 or self.Height < 3:
            return
        
        if self.Boundary == BoundaryStyle.Rounded:
            topLeft = u'\u256D'
            topRight = u'\u256E'
            bottomRight = u'\u256F'
            bottomLeft = u'\u2570'

            horizontal = u'\u2500'
            vertical = u'\u2502'
        elif self.Boundary == BoundaryStyle.Single:
            topLeft = u'\u250C'
            topRight = u'\u2510'
            bottomRight = u'\u2518'
            bottomLeft = u'\u2514'

            horizontal = u'\u2500'
            vertical = u'\u2502'
        elif self.Boundary == BoundaryStyle.Double:
            topLeft = u'\u2554'
            topRight = u'\u2557'
            bottomRight = u'\u255D'
            bottomLeft = u'\u255A'

            horizontal = u'\u2550'
            vertical = u'\u2551'

        self.Text[0][0] = topLeft
        for i in range(1, self.Width - 1):
            self.Text[0][i] = horizontal
        self.Text[0][self.Width - 1] = topRight
        for i in range(1, self.Height - 1):
            self.Text[i][self.Width - 1] = vertical
        self.Text[self.Height - 1][self.Width - 1] = bottomRight
        for i in range(1, self.Width - 1):
            self.Text[self.Height - 1][i] = horizontal
        self.Text[self.Height - 1][0] = bottomLeft
        for i in range(1, self.Height - 1):
            self.Text[i][0] = vertical