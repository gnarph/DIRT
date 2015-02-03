# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

colors = ['#ED1C24', '#F7941D', '#0000FF', '#39B54A', '#00AEEF', '#662D91']

class MyHighlighter(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(MyHighlighter, self).__init__(parent)
        self.setReadOnly(True)
        # Setup the text editor
        text = """In this text I want to hi5年发售ghlight this word and only
        this word.\n""" +\
        """Any other word shouldn't be highlighted 定于2015年发售 并一同公开了繁 ali"""
        text = text.decode('utf-8')
        self.setText(text)
        cursor = self.textCursor()
        # Setup the desired format for matches
        format = QtGui.QTextCharFormat()
        color = QtGui.QColor()
        # color.setNamedColor("#FFFF00")
        # format.setBackground(QtGui.QBrush(color))
        # Setup the regex engine
        pattern = "5年发"
        pattern = pattern.decode('utf-8')
        regex = QtCore.QRegExp(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.toPlainText(), pos)
        color_index = 0
        while (index != -1):
            # Select the matched text and apply the desired format
            cursor.setPosition(index)
            cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                                QtGui.QTextCursor.KeepAnchor, pattern.__len__())
            color.setNamedColor(colors[color_index % colors.__len__()])
            color_index += 1
            format.setForeground(QtGui.QBrush(color))
            cursor.mergeCharFormat(format)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.toPlainText(), pos)


if __name__ == "__main__":
    import sys
    a = QtGui.QApplication(sys.argv)
    t = MyHighlighter()
    t.show()
    sys.exit(a.exec_())