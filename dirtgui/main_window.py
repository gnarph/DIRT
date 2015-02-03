#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
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
    def newWindow(self):
        self.myOtherWindow = MainWindow()
        self.myOtherWindow.show()


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
        self.setWindowTitle('mainwindow')

        # ------------------------------------------------------
        #set central Widget to fill out the rest space
        self.lay_out = Layout(self)
        self.setCentralWidget(self.lay_out)

        # ------------------------------------------------------
        #file menu: open
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.display_comparison)

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


    def display_comparison(self):
        """
        Displays both the focus and match document
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/test')

        f = open(fname, 'r')

        with f:
            data = f.read()

            #to avoid garbage character when decoding other languages
            data = data.decode('utf-8')

            #set the text to TextEdit
            self.lay_out.f_frame.grid.textEdit.setText(data)
            self.lay_out.f_frame.grid.textEdit.setHtml(data)

        self.display_match()


    def display_match(self):
        """
        Displays the match document
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/temp1')
        f = open(fname, 'r')

        '''from models.document import Document
        doc = Document.from_json(fname)
        data = doc.raw_body
        data = data.decode('utf-8')
        self.lay_out.m_frame.grid.textEdit.setText(data)
        f.close()
        return'''


        with f:
            data = f.read()

            #to avoid garbage character when decoding other languages
            data = data.decode('utf-8')

            #set the text to TextEdit
            self.lay_out.m_frame.grid.textEdit.setText(data)


    def closeEvent(self, event):
        #message box: prevent accidently shut down
        reply = QtGui.QMessageBox.question(self,
                                           'Warning', "Are you sure to quit?",
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



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
    def __init__(self, parent, header):
        super(Grid, self).__init__(parent)

        # ------------------------------------------------------
        # Widgets

        # Labels
        header = QtGui.QLabel(header)
        location = QtGui.QLabel('Location :')
        title = QtGui.QLabel('Title :')
        author = QtGui.QLabel('Author :')
        #text = QtGui.QLabel('Text :')

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
        # QtGui.QTableWidget.locationEdit.setReadOnly(True)
        # QtGui.QTableWidget.titleEdit.setReadOnly(True)
        # QtGui.QTableWidget.authorEdit.setReadOnly(True)
        self.textEdit.setReadOnly(True)

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
        self.addWidget(QtGui.QTableWidget.textEdit, 4, 1, 10, 1)


class Frame(QtGui.QFrame):
    """
    Creates a frame from a grid layout
    Param: self, title of the frame
    """
    def __init__(self, parent, header):
        super(Frame, self).__init__(parent)

        self.grid = Grid(self, header)

        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setLayout(self.grid)


        # Set Location, Title, Author to be displayed
        self.grid.locationEdit.setText('Here')
        self.grid.titleEdit.setText('Hi')
        self.grid.authorEdit.setText('Me')



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
        # Result Table Frame

        result_table = Table()
        table_label = QtGui.QLabel('RESULTS TABLE')
        table_label.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        table_label.setAlignment(QtCore.Qt.AlignCenter)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(table_label)
        vbox.addWidget(result_table)
        # vbox.setAlignment(QtCore.Qt.AlignCenter)
        table_frame = QtGui.QFrame(self)
        table_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        table_frame.setLayout(vbox)

        # ------------------------------------------------------
        # Comparison Frames

        self.f_frame = Frame(self, 'FOCUS')
        self.m_frame = Frame(self, 'MATCH')

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


def main():
    app = QtGui.QApplication(sys.argv)
    mw = RunningWindow()
    mw.setGeometry(300, 300, 250, 150)
    mw.setWindowTitle('DIRT')
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
