from ScreenManager import Box, ScreenManager
from enum import Enum, auto

class BoundaryStyle(Enum):
    Single = auto()
    Double = auto()
    Rounded = auto()

class BoundedBox(Box):
    def __init__(self, x, y, width, height, boundary = None):
        Box.__init__(self, x, y, width, height)
        self.Boundary = boundary
        self.Text = [[self.Char for w in range(self.Width)] for h in range(self.Height)]
        self.writeBoundary()
        
    def writeBoundary(self):
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

    def handleInput(self, x):
        pass
        

if __name__ == '__main__':
    manager = ScreenManager()
    root = Box(0, 0, *manager.getScreenSize())
    box1 = BoundedBox(0, 0, 10, 10, boundary = BoundaryStyle.Single)
    box2 = BoundedBox(5, 5, 10, 10, boundary = BoundaryStyle.Rounded)
    root.addChild(box1)
    root.addChild(box2)
    manager.setRoot(root)
    manager.run()