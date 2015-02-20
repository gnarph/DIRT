#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class RunningWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.layout = GridLayout(self)
        self.setCentralWidget(self.layout)

        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('DiRT Startup')    
        self.show()


class GridLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # Create the QVBoxLayout that lays out the whole form
        self.layout = QVBoxLayout()

        # Create the form layout that manages the labeled controls
        self.form_layout = QFormLayout()

        self.fileInputEdit = QLineEdit(self)
        self.form_layout.addRow('Input Files:',self.fileInputEdit)

        self.prepDirEdit = QLineEdit(self)
        self.form_layout.addRow('Preprocessed Directory:',self.prepDirEdit)

        self.outDirEdit = QLineEdit(self)
        self.form_layout.addRow('Output Directory:',self.outDirEdit)

        # Add the form layout to the main VBox layout
        self.layout.addLayout(self.form_layout)
 
        # Add stretch to separate the form layout from the button
        self.layout.addStretch(1)

        # Create a horizontal box layout to hold the button
        self.button_box = QHBoxLayout()

        # Add stretch to push the button to the far right
        self.button_box.addStretch(1)

       # Create the build button with its caption
        self.startButton = QPushButton('DiRT Start', self)
 
        # Add it to the button box
        self.button_box.addWidget(self.startButton)
 
        # Add the button box to the bottom of the main VBox layout
        self.layout.addLayout(self.button_box) 

        
        self.setLayout(self.layout)

        self.connect(self.startButton, SIGNAL('clicked()'), self.newWindow)

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
    
