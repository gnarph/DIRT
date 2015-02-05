#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from dirtgui.main_layout import MainLayout
from dirtgui.select_from_list_dialog import SelectFromListDialog
from models.match_set_index import MatchSetIndex
from models import match_set_factory


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
        self.other_window = MainWindow()
        self.other_window.show()


class MainWindow(QtGui.QMainWindow):
    """
    The main window GUI for DIRT.
    Includes some shortcut keys
    """

    def _set_initial_window_size(self):
        self.resize(350, 250)

    def _fill_with_central_widget(self):
        self.layout = MainLayout(self)
        self.setCentralWidget(self.layout)

    def _setup_open_file_menu(self):
        open_file = QtGui.QAction(QtGui.QIcon('open.png'), 'Open MatchSet', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open new File')
        open_file.triggered.connect(self.select_match_set)

        open_index = QtGui.QAction(QtGui.QIcon('nope.png'), 'Open MatchIndex', self)
        open_index.setStatusTip('Open matchindex')
        open_index.triggered.connect(self.select_match_index)
        return open_file, open_index

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

    def _attach_file_menu_items(self, *args):
        menu_bar = self.menuBar()
        f = menu_bar.addMenu('&File')
        for a in args:
            f.addAction(a)

    def _attach_toolbar_actions(self, ext):
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(ext)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self._set_initial_window_size()
        self._fill_with_central_widget()

        open_file, open_index = self._setup_open_file_menu()
        ext = self._setup_exit_file_menu()

        self.statusBar()

        self._attach_file_menu_items(ext, open_file, open_index)
        self._attach_toolbar_actions(ext)

    def select_match_index(self):
        window_title = "Select match index"
        dir_name = QtGui.QFileDialog.getExistingDirectory(self,
                                                          window_title)
        msi = MatchSetIndex(str(dir_name))
        names = msi.get_all_file_names()
        focus, accepted = SelectFromListDialog.get_selected(names)
        if accepted:
            # chose a focus document
            ms_names = msi.set_names_for_focus(focus)
            to_view, accepted = SelectFromListDialog.get_selected(ms_names)
            if accepted:
                # TODO: display first matchset
                # allow others to be selected from the results table
                self.display_match_set(to_view)
                all_docs = msi.get_all_matched_documents(focus)
                results = self.layout.results_table
                results.populate(all_docs)

    def display_match_set(self, file_name):
        ms = match_set_factory.from_json(file_name)
        if file_name not in ms.alpha_doc.raw_file_name:
            ms.swap_alpha_beta()

        focus = ms.alpha_doc
        self.layout.f_frame.grid.set_document(focus.raw_file_name)
        self.layout.f_frame.grid.locationEdit.setText(focus.file_name)

        match = ms.beta_doc
        self.layout.m_frame.grid.set_document(match.raw_file_name)
        self.layout.m_frame.grid.locationEdit.setText(match.file_name)

        # Load matches
        match_layout = self.layout.m
        match_layout.match_file = file_name
        match_layout.setup_matches_list(file_name)
        alpha = 'alpha_passage'
        beta = 'beta_passage'
        self.layout.f_frame.grid.highlight_document(file_name, alpha)
        self.layout.m_frame.grid.highlight_document(file_name, beta)

    def select_match_set(self):
        window_title = "Select match set"
        file_name = QtGui.QFileDialog.getOpenFileName(self,
                                                      window_title,
                                                      '')
        self.display_match_set(str(file_name))

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
