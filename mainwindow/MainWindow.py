#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui


class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):


        #Menu Bar
        #self.textEdit = QtGui.QTextEdit()
        #self.setCentralWidget(self.textEdit)
        #self.statusBar()

     
        #rw = RunWidget()

        #the layout of the labels
        location = QtGui.QLabel('Location')
        title = QtGui.QLabel('Title')
        author = QtGui.QLabel('Author')
        review = QtGui.QLabel('Review')

        locationEdit = QtGui.QLineEdit()
        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QTextEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(location, 1, 0)
        grid.addWidget(locationEdit, 1, 1)

        grid.addWidget(title, 2, 0)
        grid.addWidget(titleEdit, 2, 1)

        grid.addWidget(author, 3, 0)
        grid.addWidget(authorEdit, 3, 1)

        grid.addWidget(review, 4, 0)
        grid.addWidget(reviewEdit, 4, 1, 6, 1)
        
        self.setLayout(grid)

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)      
        
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('DiRT')    
        self.show()

    def showDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            self.textEdit.setText(data) 


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
