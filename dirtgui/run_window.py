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

        # The skipping character options
        self.gap_option = ['0','1','2','3','4','5']

        # Create and fill the combo box to choose the skipping character
        self.gap_length = QComboBox(self)
        self.gap_length.addItems(self.gap_option)

        # Add it to the form layout with a label
        self.form_layout.addRow('Gap Length:', self.gap_length)

        # The mimimum match lengths option
        self.match_option = ['1','2','3','4','5','6','7','8','9']

        # Create and fill the combo box to choose the skipping character
        self.minimum_match_length = QComboBox(self)
        self.minimum_match_length.addItems(self.match_option)

        # Add it to the form layout with a label
        self.form_layout.addRow('Minimum Match Length:', self.minimum_match_length)

        # Create and add the label to show the greeting text
        self.option = QLabel('', self)
        self.form_layout.addRow('Options', self.option)
 
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

        # Link to the MainWindow
        self.connect(self.startButton, SIGNAL('clicked()'), self.option_set)


    def newWindow(self):
        self.other_window = MainWindow()
        self.other_window.show()

    def option_set(self):
        # Show the constructed option
        self.option.setText('%s, %s' %(self.gap_option[self.gap_length.currentIndex()],self.match_option[self.minimum_match_length.currentIndex()]))

        

def main():
    app = QtGui.QApplication(sys.argv)
    rw = RunningWindow()
    rw.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 
    
