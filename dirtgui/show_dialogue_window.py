__author__ = 'welcome vince'

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QMainWindow):
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
        #file menu: exit
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')

        # ------------------------------------------------------
        #file menu: open
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        # ------------------------------------------------------
        #exit when 'exit' is triggered
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.statusBar()

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        file.addAction(openFile)

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


class Layout(QtGui.QWidget):
    def __init__(self,parent):
        super(Layout, self).__init__(parent)

        # ------------------------------------------------------
        # Focus Document Widgets
        f_label = QtGui.QLabel('FOCUS')
        f_location = QtGui.QLabel('Location :')
        f_title = QtGui.QLabel('Title :')
        f_author = QtGui.QLabel('Author :')
        f_text = QtGui.QLabel('Text :')

        self.f_locationEdit = QtGui.QLineEdit()
        self.f_titleEdit = QtGui.QLineEdit()
        self.f_authorEdit = QtGui.QLineEdit()
        self.f_textEdit = QtGui.QTextEdit()

        # ------------------------------------------------------
        # Match Document Widgets

        m_label = QtGui.QLabel('MATCH')
        m_location = QtGui.QLabel('Location :')
        m_title = QtGui.QLabel('Title :')
        m_author = QtGui.QLabel('Author :')
        m_text = QtGui.QLabel('Text :')

        self.m_locationEdit = QtGui.QLineEdit()
        self.m_titleEdit = QtGui.QLineEdit()
        self.m_authorEdit = QtGui.QLineEdit()
        self.m_textEdit = QtGui.QTextEdit()

        # ------------------------------------------------------
        # Focus Document Layout

        f_grid = QtGui.QGridLayout()
        f_grid.setSpacing(10)
        f_grid.addWidget(f_label)

        f_grid.addWidget(f_location, 1, 0)
        f_grid.addWidget(self.f_locationEdit, 1, 1, 2, 1)

        f_grid.addWidget(f_title, 2, 0)
        f_grid.addWidget(self.f_titleEdit, 2, 1, 2, 1)

        f_grid.addWidget(f_author, 3, 0)
        f_grid.addWidget(self.f_authorEdit, 3, 1, 2, 1)

        f_grid.addWidget(f_text, 4, 0)
        f_grid.addWidget(self.f_textEdit, 4, 1, 10, 1)

        # ------------------------------------------------------
        # Match Document Layout

        m_grid = QtGui.QGridLayout()
        m_grid.setSpacing(10)

        m_grid.addWidget(m_label)

        m_grid.addWidget(m_location, 1, 0)
        m_grid.addWidget(self.m_locationEdit, 1, 1)

        m_grid.addWidget(m_title, 2, 0)
        m_grid.addWidget(self.m_titleEdit, 2, 1)

        m_grid.addWidget(m_author, 3, 0)
        m_grid.addWidget(self.m_authorEdit, 3, 1)

        m_grid.addWidget(m_text, 4, 0)
        m_grid.addWidget(self.m_textEdit, 4, 1, 10, 1)

        # ------------------------------------------------------
        # Result Table

        result_table = QtGui.QTableWidget(self)
        result_table.setRowCount(10)
        result_table.setColumnCount(4)

        headers = ['Match Title', 'Author', '# of Matches',
                   'Match %']

        result_table.setColumnWidth(0,200)
        result_table.setColumnWidth(1,200)
        result_table.setColumnWidth(2,80)
        result_table.setColumnWidth(3,80)
        result_table.setColumnWidth(4,80)

        result_table.horizontalHeader().setStretchLastSection(True)
        result_table.setAlternatingRowColors(True)
        result_table.setHorizontalHeaderLabels(headers)
        result_table.setSortingEnabled(True)

        # ------------------------------------------------------
        # Frames

        f_frame = QtGui.QFrame(self)
        f_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        f_frame.setLayout(f_grid)

        m_frame = QtGui.QFrame(self)
        m_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        m_frame.setLayout(m_grid)

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
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('gtk+'))




def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.setGeometry(500, 200, 700, 600)
    mw.setWindowTitle('DIRT')
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
