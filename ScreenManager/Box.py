class Box:
    def __init__(self, x, y, width, height):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
    
    def draw(self):
        raise NotImplementedError()
