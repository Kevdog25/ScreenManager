from ScreenManager import BoundedBox

class TextBox(BoundedBox):
    def __init__(self, innerText, editable = True, *args, **kwargs):
        BoundedBox.__init__(self, *args, **kwargs)
        self.Editable = editable
        self.InnerText = innerText

    def writeText(self):
        words = self.InnerText.split()
        lengthLeft = self.Width - 2
        row, col = 1, 1
        for w in words:
            if lengthLeft >= len(w):
                self.Text[row][col:col+len(w)] = w
                lengthLeft = lengthLeft - len(w)
                col = col + len(w)

    def writeString(self, row, col, s):
        rows, cols = self.Height - 2, self.Width - 2

        remainingChars = (rows - row) * (cols) + (cols - col)
        if len(s) > remainingChars:
            return False, row, col
        
        while len(s) > 0:
            writingLength = min(len(s), cols - col)
            self.Text[row][col:(col + writingLength)] = s[:writingLength]
            s = s[writingLength:]
            col = col + writingLength
            if col >= cols:
                col = col % cols + 1
                row += 1

        return True, row, col

    def onKeyDown(self, event):
        if event.Char and event.Char != '\t':
            if event.Char == '\x08':
                self.InnerText = self.InnerText[:-1]
            else:
                self.InnerText += event.Char
            self.writeString(1, 1, self.InnerText)
            self.dirty()
        return True
