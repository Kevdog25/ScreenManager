class Screen:
    def __init__(self, width, height):
        self.Boxes = []
        self.IsDirty = True
        self.Width = width
        self.Height = height
        self.Text = [[' ' for w in range(self.Width)] for h in range(self.Height)]

    def addBox(self, box):
        self.Boxes.append(box)

    def update(self):
        for box in self.Boxes:
            boxText = box.draw()
            for y, row in enumerate(boxText):
                if y + box.Y >= self.Height or y + box.Y < 0:
                    continue
                for x, cell in enumerate(row):
                    if x + box.X >= self.Width or x + box.X < 0:
                        continue
                    self.Text[y + box.Y][x + box.X] = cell
        self.IsDirty = False
        return

    def handleInput(self, x):
        print(x)
        pass
    
    def draw(self):
        print(u'\n'.join(u''.join(r) for r in self.Text))

            
        
    