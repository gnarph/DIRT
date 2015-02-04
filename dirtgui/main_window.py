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
        open_file = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open new File')
        open_file.triggered.connect(self.display_match_set)
        return open_file

    def _setup_exit_file_menu(self):
        # ------------------------------------------------------
        # file menu: exit
        ext = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        ext.setShortcut('Ctrl+Q')
        ext.setStatusTip('Exit application')
        # ------------------------------------------------------
        #exit when 'exit' is triggered
        self.connect(ext, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        return ext

    def _attach_file_menu_items(self, ext, openFile):
        menubar = self.menuBar()
        f = menubar.addMenu('&File')
        f.addAction(openFile)
        f.addAction(ext)

    def _attach_toolbar_actions(self, ext):
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(ext)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self._set_initial_window_size()
        self._fill_with_central_widget()

        openFile = self._setup_open_file_menu()
        ext = self._setup_exit_file_menu()

        self.statusBar()

        self._attach_file_menu_items(ext, openFile)
        self._attach_toolbar_actions(ext)

    def display_match_set(self):
        window_title = "Select match set"
        file_name = QtGui.QFileDialog.getOpenFileName(self,
                                                      window_title,
                                                      '')
        from models import match_set_factory
        ms = match_set_factory.from_json(file_name)
        focus = ms.alpha_doc
        self.lay_out.f_frame.grid.set_document(focus.raw_file_name)
        self.lay_out.f_frame.grid.locationEdit.setText(focus.file_name)
        match = ms.beta_doc
        self.lay_out.m_frame.grid.set_document(match.raw_file_name)
        self.lay_out.m_frame.grid.locationEdit.setText(match.file_name)

        # Load matches
        match_layout = self.lay_out.m
        match_layout.match_file = file_name
        match_layout.setup_matches_list(file_name)

        print self.lay_out.m.match_file
        alpha = 'alpha_passage'
        beta = 'beta_passage'
        self.lay_out.f_frame.grid.highlight_document(file_name, alpha)
        self.lay_out.m_frame.grid.highlight_document(file_name, beta)

    def display_focus(self):
        """
        Displays both the focus and match document
        """
        window_title = "Open Focus Document"
        fname = QtGui.QFileDialog.getOpenFileName(self, window_title,
                                                  '')

        self.lay_out.f_frame.grid.set_document(fname)
        self.lay_out.f_frame.grid.locationEdit.setText(fname)

        self.display_match()

    def display_match(self):
        """
        Displays the match document
        """
        window_title = "Open Match Document"
        fname = QtGui.QFileDialog.getOpenFileName(self, window_title,
                                                  '')

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
