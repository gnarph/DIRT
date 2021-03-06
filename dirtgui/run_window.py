#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import *

import DIRT

MW = 300

INPUT_DIR_TT = u'Select directory containing corpus'
INPUT_FILE_TT = u'Select file listing corpus files'
PREP_DIR_TT = u'Select directory for storing preprocessed texts'
OUTPUT_DIR_TT = u'Select directory for storing output files'
GAP_LENGTH_TT = u'Number of consecutive non-matching characters to ignore'
MATCH_LENGTH_TT = u'Minimum length of match'
RUN_TT = u'Run processing (may take a long time)'
LANGUAGE_TT = u'3 character iso code of corpus language'


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class Worker(QtCore.QThread):
    finished = QtCore.pyqtSignal()

    def __init__(self, parsed_args=None):
        super(Worker, self).__init__()
        self.parsed_args = parsed_args

    def run(self):
        DIRT.main(self.parsed_args)
        self.finished.emit()


class RunningWindow(QDialog):

    def __init__(self, parent=None):
        super(RunningWindow, self).__init__(parent)

        self.layout = GridLayout(self)

        self.setMinimumWidth(500)
        self.setMinimumHeight(700)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.MinimumExpanding)
        self.setSizeGripEnabled(True)
        self.setWindowTitle('Run Processing')
        self.setModal(True)
        self.setStyleSheet("background-color: rgb(245,247,255);")


class GridLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.thread = None

        # Create the QVBoxLayout that lays out the whole form
        self.layout = QVBoxLayout()

        # Create the form layout that manages the labeled controls
        self.form_layout = QFormLayout()

        # Create the build button with its caption
        self.input_file_field = QLineEdit(self)
        self.input_file_field.setMinimumWidth(MW)
        self.input_file_field.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                            QtGui.QSizePolicy.Expanding)
        self.form_layout.addRow('Input File/Directory:', self.input_file_field)
        self.btn_input_file = QPushButton('Input File', self)
        self.btn_input_file.setToolTip(INPUT_FILE_TT)
        self.form_layout.addWidget(self.btn_input_file)
        self.btn_input_dir = QPushButton('Input Directory', self)
        self.btn_input_dir.setMinimumWidth(MW)
        self.btn_input_dir.setToolTip(INPUT_DIR_TT)
        self.form_layout.addWidget(self.btn_input_dir)

        self.blank_line = QLabel('', self)
        self.form_layout.addRow('', self.blank_line)

        self.preprocessed_dir_field = QLineEdit(self)
        self.form_layout.addRow('Preprocessed Directory:', self.preprocessed_dir_field)
        self.btn_preprocessed_dir = QPushButton('Preprocessed Location', self)
        self.btn_preprocessed_dir.setToolTip(PREP_DIR_TT)
        self.form_layout.addWidget(self.btn_preprocessed_dir)
        self.blank_line1 = QLabel('', self)
        self.form_layout.addRow('', self.blank_line1)

        self.output_dir_field = QLineEdit(self)
        self.form_layout.addRow('Output Directory:', self.output_dir_field)
        self.btn_output_dir = QPushButton('Output Location', self)
        self.btn_output_dir.setToolTip(OUTPUT_DIR_TT)
        self.form_layout.addWidget(self.btn_output_dir)
        self.blank_line2 = QLabel('', self)
        self.form_layout.addRow('', self.blank_line2)

        # Add the form layout to the main VBox layout
        self.layout.addLayout(self.form_layout)

        # Create and fill the combo box to choose the skipping character
        self.gap_length = QLineEdit(self)
        self.gap_length.setToolTip(GAP_LENGTH_TT)

        # Add it to the form layout with a label
        self.form_layout.addRow('Gap Length:', self.gap_length)

        # Create and fill the combo box to choose the skipping character
        self.minimum_match_length = QLineEdit(self)
        self.minimum_match_length.setToolTip(MATCH_LENGTH_TT)

        # Add it to the form layout with a label
        self.form_layout.addRow('Minimum Match Length:', self.minimum_match_length)

        # Add stretch to separate the form layout from the button
        self.layout.addStretch(1)

        # Create a horizontal box layout to hold the button
        self.button_box = QHBoxLayout()

        # Add stretch to push the button to the far right
        self.button_box.addStretch(1)

        # Create the build button with its caption
        self.btn_run = QPushButton('DiRT Start', self)
        self.btn_run.setToolTip(RUN_TT)

        # Add it to the button box
        self.button_box.addWidget(self.btn_run)

        # Add the button box to the bottom of the main VBox layout
        self.layout.addLayout(self.button_box)

        self.setLayout(self.layout)

        supported_languages = ['zhi', 'eng']
        self.language_select = QComboBox(self)
        self.language_select.addItems(supported_languages)
        self.language_select.setToolTip(LANGUAGE_TT)
        self.form_layout.addRow('Language: ', self.language_select)

        on_click = SIGNAL('clicked()')
        # Link to the DirtStart Button
        self.connect(self.btn_run, on_click, self.run)

        # Link Location Buttons
        self.connect(self.btn_input_file, on_click, self.select_input_file)
        self.connect(self.btn_input_dir, on_click, self.select_input_dir)
        self.connect(self.btn_preprocessed_dir, on_click, self.select_preprocessed_directory)
        self.connect(self.btn_output_dir, on_click, self.select_output_directory)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 1)
        self.progress_bar.hide()
        self.form_layout.addRow('Progress: ', self.progress_bar)

        self.adjustSize()

    def run(self):
        input_loc = unicode(self.input_file_field.text())
        prep_loc = unicode(self.preprocessed_dir_field.text())
        out_loc = unicode(self.output_dir_field.text())
        language = unicode(self.language_select.currentText())
        gap_length = int(self.gap_length.text())
        match_length = int(self.minimum_match_length.text())

        args = AttributeDict()
        args.input = input_loc
        args.preprocessed_dir = prep_loc
        args.output_dir = out_loc
        args.language = language
        args.comparator = u'simple'
        args.gap_length = gap_length
        args.match_length = match_length
        args.verbose = True
        args.gui = False
        args.parallel = True

        self.progress_bar.setRange(0, 0)
        self.progress_bar.show()

        self.thread = Worker(parsed_args=args)
        self.thread.finished.connect(self.done)
        self.thread.start()

    def done(self):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        t = self.thread
        self.thread = None
        t.quit()

    def select_input_file(self):
        dialog = QFileDialog()
        file_name = dialog.getOpenFileName(self, "Open")
        self.input_file_field.setText(file_name)

    def select_input_dir(self):
        dialog = QFileDialog()
        input_dir = dialog.getExistingDirectory(self, "Open")
        self.input_file_field.setText(input_dir)

    def select_preprocessed_directory(self):
        preprocessed_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.preprocessed_dir_field.setText(preprocessed_dir)

    def select_output_directory(self):
        output_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.output_dir_field.setText(output_dir)
