from ScreenManager import BoundedBox
import re

class TextBox(BoundedBox):
    def __init__(self, innerText = '', editable = True, *args, **kwargs):
        BoundedBox.__init__(self, *args, **kwargs)
        self.Editable = editable
        self.canFocus = editable
        self._innerText = ''
        self.cursor = 0
        self._events = {
            'onTextChange' : []
        }
        if self.Boundary is None:
            self.textWidth = self.Width
            self.textHeight = self.Height
        else:
            self.textWidth = self.Width - 2
            self.textHeight = self.Height - 2
        
        
    def onTextChange(self, func):
        self._events['onTextChange'].append(func)
    def raiseTextChange(self):
        text = self.InnerText
        for f in self._events['onTextChange']:
            f(text)
    def maxLength(self):
        return (self.textHeight) * (self.textWidth)

    @property
    def InnerText(self):
        return self._innerText.replace(chr(0), '')
    @InnerText.setter
    def InnerText(self, text):
        self.cursor = 0
        self._innerText = ''
        for c in text:
            self.addChar(c)
    
    def setChar(self, row, col, char):
        if self.Boundary is not None:
            row += 1
            col += 1
        self.Buffer[row][col] = char
    
    def addChar(self, char):
        if self._innerText[-1:] in (' ', chr(0)) or char == ' ':
            self.writeWord(char)
            return
        lastWord = re.split('[ {}]+'.format(chr(0)),self._innerText)[-1]
        self._innerText = self._innerText[:-len(lastWord)]
        self.cursor -= len(lastWord)
        lastWord = lastWord + char
        self.writeWord(lastWord)
    
    def backspace(self):
        if self.cursor == 0:
            return
        if self._innerText[-1] == ' ':
            self.cursor -= 1
            self._innerText = self._innerText[:-1]
            return
        
        lastWord = re.split('[ {}]+'.format(chr(0)),self._innerText)[-1][:-1]
        beforeLastWord = len(self._innerText) - len(lastWord) - 1
        self._innerText = self._innerText[:beforeLastWord].rstrip(chr(0))
        for row, col in self.positions(beforeLastWord, self.cursor):
            self.setChar(row, col, ' ')
        self.cursor = len(self._innerText)
        self.writeWord(lastWord)
        
    def writeWord(self, word):
        word = word[:(self.textWidth)][:(self.maxLength() - self.cursor)]
        
        row, col = self.position(self.cursor)
        if len(word) > (self.textWidth - col + 1):
            self.newLine()
        for v in word:
            row, col = self.position(self.cursor)
            self.setChar(row, col, v)
            self.cursor += 1
        self._innerText += word
        return
        
    def newLine(self):
        row, col = self.position(self.cursor)
        if row < self.textHeight - 1:
            nextCursor = (row + 1) * (self.textWidth)
            for r, c in self.positions(self.cursor, nextCursor):
                self.setChar(r, c, ' ')
                self._innerText += chr(0)
            self.cursor = nextCursor
        
    def positions(self, start, end):
        for i in range(start, min(end, self.maxLength())):
            yield self.position(i)
    def position(self, i):
        return (i // (self.textWidth)), (i % (self.textWidth))
    
    def onKeyDown(self, event):
        if event.Char and event.Char not in ['\t', None]:
            #print(ord(event.Char))
            if event.Char == chr(8):
                self.backspace()
            else:
                self.addChar(event.Char)
            self.raiseTextChange()
            self.dirty()
        return True
