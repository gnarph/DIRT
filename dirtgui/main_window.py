__author__ = 'welcome vince'

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
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
        openFile.triggered.connect(self.showDialog)

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

    def showDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        f = open(fname, 'r')

        with f:
            data = f.read()

            #to avoid garbage character when decoding other languages
            data = data.decode('utf-8')

            #set the text to TextEdit
            self.lay_out.reviewEdit.setText(data)


class Table(QtGui.QTableWidget):
    """
    Creates a table that self populates
    """

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setColumnCount(5)
        self.populate()

        headers = ['Match Title', 'Author(s)', '# of Matches',
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


    def populate(self):
        self.setRowCount(10)

        for i in range(10):
            for j,l in enumerate(string.letters[:5]):
                self.setItem(i, j, QtGui.QTableWidgetItem(l))

        self.setRowCount(10)
        for i in range(10):
            for j,l in enumerate(string.letters[:5]):
                self.setItem(i, j, QtGui.QTableWidgetItem(l))

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

        label = QtGui.QLabel(header)
        location = QtGui.QLabel('Location :')
        title = QtGui.QLabel('Title :')
        author = QtGui.QLabel('Author :')
        text = QtGui.QLabel('Text :')

        QtGui.QTableWidget.locationEdit = QtGui.QLineEdit()
        QtGui.QTableWidget.titleEdit = QtGui.QLineEdit()
        QtGui.QTableWidget.authorEdit = QtGui.QLineEdit()
        QtGui.QTableWidget.textEdit = QtGui.QTextEdit()

        QtGui.QTableWidget.locationEdit.setReadOnly(True)       # set to READ-only
        QtGui.QTableWidget.titleEdit.setReadOnly(True)
        QtGui.QTableWidget.authorEdit.setReadOnly(True)
        QtGui.QTableWidget.textEdit.setReadOnly(True)

        # ------------------------------------------------------
        # Grid Layout

        self.setSpacing(10)
        self.addWidget(label)

        self.addWidget(location, 1, 0)
        self.addWidget(QtGui.QTableWidget.locationEdit, 1, 1)

        self.addWidget(title, 2, 0)
        self.addWidget(QtGui.QTableWidget.titleEdit, 2, 1)

        self.addWidget(author, 3, 0)
        self.addWidget(QtGui.QTableWidget.authorEdit, 3, 1)

        self.addWidget(text, 4, 0)
        self.addWidget(QtGui.QTableWidget.textEdit, 4, 1, 10, 1)


class Frame(QtGui.QFrame):
    """
    Creates a frame from a grid layout
    Param: self, title of the frame
    """
    def __init__(self, parent, header):
        super(Frame, self).__init__(parent)

        grid = Grid(self, header)

        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setLayout(grid)


class Layout(QtGui.QWidget):
    """
    Splitter layout that separates frames
    and allows to adjust the size relatively
    then puts everything in a horizontal layout
    Theme: Cleanlooks
    """

    def __init__(self,parent):
        super(Layout, self).__init__(parent)

        # ------------------------------------------------------
        # Result Table

        result_table = Table()

        # ------------------------------------------------------
        # Frames

        f_frame = Frame(self, 'FOCUS')
        m_frame = Frame(self, 'MATCH')

        # ------------------------------------------------------
        # Splitter Layout

        hbox = QtGui.QHBoxLayout(self)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(f_frame)
        splitter1.addWidget(m_frame)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(result_table)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.setGeometry(500, 200, 700, 600)
    mw.setWindowTitle('DIRT')
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
