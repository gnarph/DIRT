#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from dirtgui.main_layout import MainLayout


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
        self.lay_out = MainLayout(self)
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
