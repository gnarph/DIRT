#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from dirtgui.document_util import doc_util as document_util
from dirtgui.document_util import document_match_util as match_util
from dirtgui.main_table import MainTable


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

    def newWindow(self):
        self.myOtherWindow = MainWindow()
        self.myOtherWindow.show()


class MainWindow(QtGui.QMainWindow):
    """
    The main window GUI for DIRT.
    Includes some shortcut keys
    """

    def _set_initial_window_size(self):
        self.resize(350, 250)

    def _fill_with_central_widget(self):
        self.lay_out = Layout(self)
        self.setCentralWidget(self.lay_out)

    def _setup_open_file_menu(self):
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.display_focus)
        return openFile

    def _setup_exit_file_menu(self):
        # ------------------------------------------------------
        # file menu: exit
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        # ------------------------------------------------------
        #exit when 'exit' is triggered
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        return exit

    def _attach_file_menu_items(self, exit, openFile):
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(openFile)
        file.addAction(exit)

    def _attach_toolbar_actions(self, exit):
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self._set_initial_window_size()
        self._fill_with_central_widget()

        openFile = self._setup_open_file_menu()
        exit = self._setup_exit_file_menu()

        self.statusBar()

        self._attach_file_menu_items(exit, openFile)
        self._attach_toolbar_actions(exit)

    def display_focus(self):
        """
        Displays both the focus and match document
        """
        window_title = "Open Focus Document"
        fname = QtGui.QFileDialog.getOpenFileName(self, window_title,
                                                  '../dirt_example/')

        passage_type = 'alpha_passage'
        self.lay_out.f_frame.grid.set_document(fname)
        self.lay_out.f_frame.grid.locationEdit.setText(fname)

        self.display_match()

    def display_match(self):
        """
        Displays the match document
        """
        window_title = "Open Match Document"
        fname = QtGui.QFileDialog.getOpenFileName(self, window_title,
                                                  './dirt_example/')

        self.lay_out.m_frame.grid.set_document(fname)
        self.lay_out.m_frame.grid.locationEdit.setText(fname)

        self.highlight_documents()

    def highlight_documents(self):
        window_title = "Open Json Match File"
        fname = QtGui.QFileDialog.getOpenFileName(self, window_title, '')

        match = self.lay_out.m
        match.match_file = fname
        match.setup_matches_list(fname)

        print self.lay_out.m.match_file
        alpha = 'alpha_passage'
        beta = 'beta_passage'
        self.lay_out.f_frame.grid.highlight_document(fname, alpha)
        self.lay_out.m_frame.grid.highlight_document(fname, beta)

    def closeEvent(self, event):
        #message box: prevent accidently shut down
        reply = QtGui.QMessageBox.question(self,
                                           'Warning',
                                           "Are you sure you want to quit?",
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Grid(QtGui.QGridLayout):
    """
    Creates a grid with Location, Title, Author, and Text READ-only display
    Param: self, title of the layout
    """
    def __init__(self, parent, header, passage_type):
        super(Grid, self).__init__(parent)

        # ------------------------------------------------------
        # Widgets

        # Labels
        header = QtGui.QLabel(header)
        location = QtGui.QLabel('Location :')
        title = QtGui.QLabel('Title :')
        author = QtGui.QLabel('Author :')
        #text = QtGui.QLabel('Text :')
        self.passage_type = passage_type

        # Label Fonts
        label_font = QtGui.QFont('', 11, QtGui.QFont.Bold)

        header.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        header.setAlignment(QtCore.Qt.AlignCenter)
        location.setFont(label_font)
        location.setAlignment(QtCore.Qt.AlignRight)
        title.setFont(label_font)
        title.setAlignment(QtCore.Qt.AlignRight)
        author.setFont(label_font)
        author.setAlignment(QtCore.Qt.AlignRight)
        #text.setFont(label_font)

        # ------------------------------------------------------
        # Text displays
        self.locationEdit = QtGui.QTableWidget.locationEdit = QtGui.QLineEdit()
        self.titleEdit = QtGui.QTableWidget.titleEdit = QtGui.QLineEdit()
        self.authorEdit = QtGui.QTableWidget.authorEdit = QtGui.QLineEdit()
        self.textEdit = QtGui.QTableWidget.textEdit = QtGui.QTextEdit()

        # Text display font
        display_font = QtGui.QFont('', 12)

        self.locationEdit.setFont(display_font)
        self.titleEdit.setFont(display_font)
        self.authorEdit.setFont(display_font)
        self.textEdit.setFont(display_font)

        # Set all text displays to READ-only
        QtGui.QTableWidget.locationEdit.setReadOnly(True)
        QtGui.QTableWidget.titleEdit.setReadOnly(True)
        QtGui.QTableWidget.authorEdit.setReadOnly(True)
        QtGui.QTableWidget.textEdit.setReadOnly(True)

        # Cursor
        #self.textEdit.setTextCursor(QtGui.QTextCursor())

        # ------------------------------------------------------
        # Position on Grid Layout

        # Header
        self.setSpacing(10)
        self.addWidget(header, 0, 1)

        # Location
        self.addWidget(location, 1, 0)
        self.addWidget(QtGui.QTableWidget.locationEdit, 1, 1)

        # Title
        self.addWidget(title, 2, 0)
        self.addWidget(QtGui.QTableWidget.titleEdit, 2, 1)

        # Author
        self.addWidget(author, 3, 0)
        self.addWidget(QtGui.QTableWidget.authorEdit, 3, 1)

        # Text
        #self.addWidget(text, 4, 0)
        self.addWidget(QtGui.QTableWidget.textEdit, 4, 0, 10, -1)

        self.file_path = ''
        self.match_file = ''

    def set_document(self, doc):
        """
        Set the document for the grid text area
        :param doc: file path of document
        :return:
        """
        text_area = self.textEdit
        document_util.open_doc(text_area, doc)

    def highlight_document(self, match_data, passage):
        """"
        Highlight the matches in a document
        :param match_data:
        :param passage:
        :return:
        """
        text_area = self.textEdit
        cursor = self.textEdit.textCursor()
        match_util.highlight_matches(text_area, cursor, match_data, passage)


class Frame(QtGui.QFrame):
    """
    Creates a frame from a grid layout
    Param: self, title of the frame
    """
    def __init__(self, parent, header):
        super(Frame, self).__init__(parent)

        if header == 'FOCUS':
            passage_type = 'alpha_passage'
        elif header == 'MATCH':
            passage_type = 'beta_passage'

        self.grid = Grid(self, header, passage_type)

        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setLayout(self.grid)

        # Set Location, Title, Author to be displayed
        # self.grid.locationEdit.setText('Here')
        # self.grid.titleEdit.setText('Hi')
        # self.grid.authorEdit.setText('Me')


class Layout(QtGui.QWidget):
    """
    Splitter layout that separates frames
    and allows to adjust the size relatively
    then puts everything in a horizontal layout
    Theme: 'cleanlooks'
    """

    def __init__(self, parent):
        super(Layout, self).__init__(parent)

        # ------------------------------------------------------
        # Comparison Frames

        self.f_frame = Frame(self, 'FOCUS')
        focus_doc_area = self.f_frame.grid.textEdit
        self.m_frame = Frame(self, 'MATCH')
        match_doc_area = self.m_frame.grid.textEdit
        self.m = match_util.DocumentMatchUtil(focus_doc_area,
                                              match_doc_area, '')

        # ------------------------------------------------------
        # Result Table Frame

        result_table = MainTable()
        table_label = QtGui.QLabel('RESULTS TABLE')
        table_label.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        table_label.setAlignment(QtCore.Qt.AlignCenter)

        navigation_bar = QtGui.QHBoxLayout()
        previous_button = QtGui.QPushButton()
        previous_button.setText('Previous')
        previous_button.clicked.connect(self.m.prev_match)
        navigation_bar.addWidget(previous_button)
        next_button = QtGui.QPushButton()
        next_button.setText('Next')
        next_button.clicked.connect(self.m.next_match)
        navigation_bar.addWidget(next_button)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(navigation_bar)
        vbox.addWidget(table_label)
        vbox.addWidget(result_table)
        # vbox.setAlignment(QtCore.Qt.AlignCenter)
        table_frame = QtGui.QFrame(self)
        table_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        table_frame.setLayout(vbox)

        # ------------------------------------------------------
        # Splitter Layout
        hbox = QtGui.QHBoxLayout(self)

        # Splits focus and match document
        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.f_frame)
        splitter1.addWidget(self.m_frame)

        # Splits text comparison from result table
        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(table_frame)

        # Putting splitter layouts into horizontal layout
        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))


def center_window(window):
    desktop = QtGui.QApplication.desktop()
    screen_dimension = QtCore.QRect(desktop.screenGeometry())
    window_width = 700
    window_height = 700
    x = (screen_dimension.width() - window_width)/2
    y = (screen_dimension.height() - window_height)/2
    window.setGeometry(x, y, window_width, window_height)


def setup_window(window):
    center_window(window)
    window.setWindowTitle('DIRT')
    window.show()
    window.raise_()


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    setup_window(mw)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
