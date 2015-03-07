#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import *

import DIRT


class RunningWindow(QDialog):

    def __init__(self, parent=None):
        super(RunningWindow, self).__init__(parent)

        self.layout = GridLayout(self)

        # self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('DiRT Startup')
        self.setModal(True)
        self.setStyleSheet("background-color: rgb(245,247,255);")


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

        # Create and fill the combo box to choose the skipping character
        self.gap_length = QLineEdit(self)

        # Add it to the form layout with a label
        self.form_layout.addRow('Gap Length:', self.gap_length)

        # Create and fill the combo box to choose the skipping character
        self.minimum_match_length = QLineEdit(self)

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
        self.connect(self.startButton, SIGNAL('clicked()'), self.run)

        # Link Location Buttons
        self.connect(self.Button1, SIGNAL('clicked()'), self.select_input_file)
        self.connect(self.Button2, SIGNAL('clicked()'), self.select_preprocessed_directory)
        self.connect(self.Button3, SIGNAL('clicked()'), self.select_output_directory)

        self.adjustSize()

    def run(self):
        gap_length = int(self.gap_length.text())
        match_length = int(self.minimum_match_length.text())
        print gap_length, match_length
        args = None
        DIRT.main(args)

    def select_input_file(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File")
        self.fileInputEdit.setText(fileName)

    def select_preprocessed_directory(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.prepDirEdit.setText(file)

    def select_output_directory(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.outDirEdit.setText(file)
