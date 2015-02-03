#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import document_util.document_util as document_util
import document_util.document_match_util as match_util

from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QMainWindow):
    """
    The main window GUI for DIRT.
    Includes some shortcut keys
    """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # ------------------------------------------------------
        #initial window size
        self.resize(350, 250)

        # ------------------------------------------------------
        #set central Widget to fill out the rest space
        self.lay_out = Layout(self)
        self.setCentralWidget(self.lay_out)

        # ------------------------------------------------------
        #file menu: open
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.display_focus)

        # ------------------------------------------------------
        #file menu: exit
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')

        # ------------------------------------------------------
        #exit when 'exit' is triggered
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.statusBar()

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(openFile)
        file.addAction(exit)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)

    def display_focus(self):
        """
        Displays both the focus and match document
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                  '../dirt_preprocessed/pre')

        match_file = self.lay_out.m.match_file
        passage_type = 'alpha_passage'
        self.lay_out.f_frame.grid.set_document(fname)
        self.lay_out.f_frame.grid.locationEdit.setText(fname)
        self.lay_out.f_frame.grid.highlight_document(match_file,
                                                     passage_type)

        self.display_match()

    def display_match(self):
        """
        Displays the match document
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                  './dirt_preprocessed/pre')
        f = open(fname, 'r')

        match_file = self.lay_out.m.match_file
        passage_type = 'beta_passage'
        self.lay_out.m_frame.grid.set_document(fname)
        self.lay_out.m_frame.grid.locationEdit.setText(fname)
        self.lay_out.m_frame.grid.highlight_document(match_file,
                                                     passage_type)


class Table(QtGui.QTableWidget):
    """
    Creates a table that self populates
    """

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setColumnCount(5)
        self.populate()

        headers = ['Match Title', 'Author(s)', 'Matches',
                   'Match %', 'Location']

        self.setColumnWidth(0,200)
        self.setColumnWidth(1,200)
        self.setColumnWidth(2,80)
        self.setColumnWidth(3,80)
        self.setColumnWidth(4,80)

        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(headers)
        self.setSortingEnabled(True)

        # Header and cell fonts
        font = QtGui.QFont('', 11, QtGui.QFont.Bold)
        self.horizontalHeader().setFont(font)
        cell_font = QtGui.QFont('', 11, QtGui.QFont.AnyStyle)
        self.setFont(cell_font)

    def populate(self):
        """
        Populates the table with elements
        """

        # Populates table with alphabetical lettering
        self.setRowCount(10)

        for i in range(10):
            for j,l in enumerate(string.letters[:5]):
                item = QtGui.QTableWidgetItem(l)
                # Line below locks the item in the cells
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, j, item)

        # Populates table using a list by column then row
        """
        entries = []
        with open('data') as input:
            for line in input:
                entries.append(line.strip().split('\t'))

        tableWidget.setRowCount(len(entries))
        tableWidget.setColumnCount(len(entries[0]))
        
        for i, row in enumerate(entries):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                tableWidget.setItem(i, j, item)
        """


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
        self.m = match_util.DocumentMatchUtil(focus_doc_area, match_doc_area,
                                    "../dirt_output/lorem__lorem2__CMP.json")

        # ------------------------------------------------------
        # Result Table Frame

        result_table = Table()
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
