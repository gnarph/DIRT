#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class RunningWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.layout = BoxLayout(self)
        self.setCentralWidget(self.layout)

        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('DiRT Startup')    
        self.show()


class BoxLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.setWindowTitle('box layout')

        startButton = QtGui.QPushButton("DiRT Start")
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(startButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.connect(startButton, SIGNAL('clicked()'), self.newWindow)


    def newWindow(self):
        self.other_window = MainWindow()
        self.other_window.show()

def main():
    app = QtGui.QApplication(sys.argv)
    rw = RunningWindow()
    rw.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 
    
