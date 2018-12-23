from ScreenManager import Box, ScreenManager
from ScreenManager import BoundedBox, TextBox

if __name__ == '__main__':
    manager = ScreenManager()
    root = Box(0, 0, *manager.getScreenSize())
    box1 = BoundedBox(0, 0, 10, 10)
    box2 = TextBox('', True, 5, 5, 10, 10)
    root.addChild(box1)
    root.addChild(box2)
    manager.setRoot(root)
    manager.run()