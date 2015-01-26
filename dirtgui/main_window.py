#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        #initial window size
        self.resize(350, 250)
        self.setWindowTitle('mainwindow')

        #set central Widget to fill out the rest space
        self.lay_out = Layout(self)
        self.setCentralWidget(self.lay_out)

        #file menu: exit
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')

        #file menu: open
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

         #exit when 'exit' is triggered
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.statusBar()

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        file.addAction(openFile)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)

    def showDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        f = open(fname, 'r')

        with f:
            data = f.read()

            #to avoid garbage character when decoding other languages
            data = data.decode('utf-8')

            #set the text to TextEdit
            self.lay_out.reviewEdit.setText(data)


class Layout(QtGui.QWidget):
    def __init__(self,parent):
        super(Layout, self).__init__(parent)

        #testing layout
        location = QtGui.QLabel('Location')
        title = QtGui.QLabel('Title')
        author = QtGui.QLabel('Author')
        review = QtGui.QLabel('Review')

        #create attributes for lay_out
        self.locationEdit = QtGui.QLineEdit()
        self.titleEdit = QtGui.QLineEdit()
        self.authorEdit = QtGui.QLineEdit()
        self.reviewEdit = QtGui.QTextEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(location, 1, 0)
        grid.addWidget(self.locationEdit, 1, 1)

        grid.addWidget(title, 2, 0)
        grid.addWidget(self.titleEdit, 2, 1)

        grid.addWidget(author, 3, 0)
        grid.addWidget(self.authorEdit, 3, 1)

        grid.addWidget(review, 4, 0)
        grid.addWidget(self.reviewEdit, 4, 1, 6, 1)

        self.setLayout(grid)


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.setGeometry(300, 300, 350, 300)
    mw.setWindowTitle('DiRT')
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
