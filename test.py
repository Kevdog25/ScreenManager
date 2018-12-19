from ScreenManager import Box, Screen, ScreenManager

class BoundedBox(Box):
    def __init__(self, x, y, width, height):
        Box.__init__(self, x, y, width, height)

    def draw(self):
        text = [['X' for w in range(self.Width)] for h in range(self.Height)]

        return text



if __name__ == '__main__':
    manager = ScreenManager()
    screen = Screen(120, 60)
    box1 = BoundedBox(0, 0, 10, 10)
    box2 = BoundedBox(30, 30, 5, 40)
    screen.addBox(box1)
    screen.addBox(box2)
    manager.setCurrent(screen)
    manager.run()