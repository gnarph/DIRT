#!/usr/bin/env python
#coding: utf-8

"""
ZetCode PyQt4 tutorial

In this example, we select a file with a
QtGui.QFileDialog and display its contents
in a QtGui.QTextEdit.

author: Jan Bodnar
website: zetcode.com
last edited: October 2011
"""

import sys
from PyQt4 import QtGui


class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'),
                                 'Open',
                                 self)
        translateFile = QtGui.QAction(QtGui.QIcon('Translate.png'),
                                      'Translate',
                                      self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(translateFile)

        fileMenu = menubar.addMenu('&Translate')

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def showDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                '/home')
        with open(fname, 'r') as f:
            data = f.read()
            #data = unicode(data,'utf8').encode('utf8')
            self.textEdit.setText(unicode(data,'utf8'))


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()