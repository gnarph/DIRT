#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class RunningWindow(QtGui.QDialog):

    def __init__(self, parent=None):
        super(RunningWindow, self).__init__(parent)

        self.layout = GridLayout(self)
        self.setModal(True)

        # self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('DiRT Startup')


class GridLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # Create the QVBoxLayout that lays out the whole form
        self.layout = QVBoxLayout()

        # Create the form layout that manages the labeled controls
        self.form_layout = QFormLayout()

        # Create the build button with its caption
        self.fileInputEdit = QLineEdit(self)
        self.form_layout.addRow('Input Files:',self.fileInputEdit)
        self.Button1 = QPushButton('Input Files Location', self)
        self.form_layout.addWidget(self.Button1)
        self.blank_line = QLabel('', self)
        self.form_layout.addRow('', self.blank_line)


        self.prepDirEdit = QLineEdit(self)
        self.form_layout.addRow('Preprocessed Directory:',self.prepDirEdit)
        self.Button2 = QPushButton('Preprocessed Location', self)
        self.form_layout.addWidget(self.Button2)
        self.blank_line1 = QLabel('', self)
        self.form_layout.addRow('', self.blank_line1)

        self.outDirEdit = QLineEdit(self)
        self.form_layout.addRow('Output Directory:',self.outDirEdit)
        self.Button3 = QPushButton('Output Location', self)
        self.form_layout.addWidget(self.Button3)
        self.blank_line2 = QLabel('', self)
        self.form_layout.addRow('', self.blank_line2)

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

        # Link to the DirtStart Button
        self.connect(self.startButton, SIGNAL('clicked()'), self.option_set)

        # Link Location Buttons
        self.connect(self.Button1, SIGNAL('clicked()'), self.location1)
        self.connect(self.Button2, SIGNAL('clicked()'), self.location2)
        self.connect(self.Button3, SIGNAL('clicked()'), self.location3)

        self.adjustSize()

    def option_set(self):
        # Show the constructed option
        self.option.setText('%s, %s' %(self.gap_option[self.gap_length.currentIndex()],self.match_option[self.minimum_match_length.currentIndex()]))

    def location1(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File")
        self.fileInputEdit.setText(fileName) 
        
    def location2(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.prepDirEdit.setText(file)
        
    def location3(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.outDirEdit.setText(file)
