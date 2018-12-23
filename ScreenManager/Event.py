class Event:
    def __init__(self):
        pass

class KeyDown(Event):
    def __init__(self, character = None, control = None, *args, **kwargs):
        if character is None and control is None:
            raise ValueError('character and control cannot both be None')
        self.Char = character
        self.Control = control
        Event.__init__(self, *args, **kwargs)
