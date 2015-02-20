#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class RunningWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        layout = QHBoxLayout()
        button = QPushButton('Click me to start!', self)
        layout.addWidget(button)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Win1")

        self.connect(button, SIGNAL('clicked()'), self.newWindow)
        self.show()

    def newWindow(self):
        self.other_window = MainWindow()
        self.other_window.show()


def main(index_dir):
    app = QtGui.QApplication(sys.argv)
    rw = RunnningWindow()
    setup_window(rw)
    rw.show()
    
    sys.exit(app.exec_())

    
