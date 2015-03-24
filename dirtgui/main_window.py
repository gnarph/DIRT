#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import document_util.document_match_util as dmu

from PyQt4 import QtGui, QtCore

from dirtgui.main_layout import MainLayout
from dirtgui.select_from_list_dialog import SelectFromListDialog
from dirtgui.run_window import RunningWindow
from models.match_set_index import MatchSetIndex
from models import match_set_factory
from utilities import path


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
        open_index = QtGui.QAction(QtGui.QIcon('nope.png'), 'Open MatchIndex', self)
        open_index.setShortcut('Ctrl+O')
        open_index.setStatusTip('Open matchindex')
        open_index.triggered.connect(self.select_match_index)

        run_dialog = QtGui.QAction('Run Dialog', self)
        run_dialog.setShortcut('Ctrl+R')
        run_dialog.triggered.connect(self.run_dialog)

        return open_index, run_dialog

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

    # def _attach_toolbar_actions(self, ext):
    #     toolbar = self.addToolBar('Exit')
    #     toolbar.addAction(ext)

    def __init__(self, index_dir=None):
        QtGui.QMainWindow.__init__(self)

        self._set_initial_window_size()
        self._fill_with_central_widget()

        open_index, run_dialog = self._setup_open_file_menu()
        ext = self._setup_exit_file_menu()

        self.statusBar()

        self._attach_file_menu_items(run_dialog, open_index, ext)
        # self._attach_toolbar_actions(ext)

        self.raise_()
        if index_dir:
            self.display_match_index(index_dir)

        self.match_set_index = None
        self.focus = None
        self.dialog = RunningWindow()

    def display_match_index(self, dir_name):
        self.match_set_index = MatchSetIndex(str(dir_name))
        msi = self.match_set_index
        names = msi.get_all_file_names()
        focus, accepted = SelectFromListDialog.get_selected(names,
                                                            title='Select Focus Document')
        if accepted:
            # chose a focus document
            self.focus = focus
            ms_names = msi.set_names_for_focus(focus)
            to_view, accepted = SelectFromListDialog.get_selected(ms_names,
                                                                  title='Select Document to Compare')
            if accepted:
                # TODO: display first matchset
                # allow others to be selected from the results table
                self.display_match_set(to_view)
                # all_docs = msi.get_all_matched_documents(focus)
                results = self.layout.results_table
                self.layout.results_table.setSortingEnabled(True)
                # TODO: should pass msi down instead
                results.populate(focus, msi)
                results.sortItems(2, QtCore.Qt.DescendingOrder)
                total_match = self.match_set_index.get_matched_document_count(focus)
                self.layout.table_label.setText('Results (%d)' % total_match)

    def select_match_index(self):
        window_title = "Select match index"
        dir_name = QtGui.QFileDialog.getExistingDirectory(self,
                                                          window_title)
        self.display_match_index(str(dir_name))

    def display_match_set(self, file_name):
        # Handle match set file itself
        if '.json' in file_name:
            ms = match_set_factory.from_json(file_name)
            if file_name not in ms.alpha_doc.raw_file_name:
                ms.swap_alpha_beta()
        else:
            # Or just the name of the file
            out_dir = self.match_set_index.out_dir
            focus_name = path.get_name(self.focus, extension=False)
            ms = match_set_factory.find_in_dir(focus_name,
                                               file_name,
                                               out_dir)

        # TODO: most of this stuff should be in DocumentGrid
        # Set the document frames
        focus = ms.alpha_doc
        self.layout.f_frame.grid.set_document(focus.pre_file_name)
        self.layout.f_frame.grid.documentPathEdit.setText(focus.file_name)
        focus_title = path.get_name(focus.file_name, False)
        self.layout.f_frame.grid.documentTitleEdit.setText(focus_title)

        match = ms.beta_doc
        self.layout.m_frame.grid.set_document(match.pre_file_name)
        self.layout.m_frame.grid.documentPathEdit.setText(match.file_name)
        match_title = path.get_name(match.file_name, False)
        self.layout.m_frame.grid.documentTitleEdit.setText(match_title)

        # Load matches
        focus_text_area = self.layout.f_frame.grid.textEdit
        match_text_area = self.layout.m_frame.grid.textEdit
        dmu.clear_highlight(focus_text_area)
        dmu.clear_highlight(match_text_area)
        self.layout.highlighter = dmu.Highlighter(focus_text_area,
                                                  match_text_area, ms)

        alpha = 'alpha'
        beta = 'beta'
        self.layout.f_frame.grid.highlight_document(ms, alpha)
        self.layout.f_frame.grid.highlighter = self.layout.highlighter
        self.layout.m_frame.grid.highlight_document(ms, beta)
        self.layout.m_frame.grid.highlighter = self.layout.highlighter

    def select_match_set(self):
        window_title = "Select match set"
        file_name = QtGui.QFileDialog.getOpenFileName(self,
                                                      window_title)
        self.display_match_set(str(file_name))

    def run_dialog(self):
        self.dialog.show()

    def closeEvent(self, event):
        #message box: prevent accidentally shut down
        reply = QtGui.QMessageBox.question(self,
                                           'Warning',
                                           "Are you sure you want to quit?",
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def click_display(self, row):
        """
        When clicked, displays the match document in the text box
        """
        item = QtGui.QTableWidget.itemAt(row, 5)
        self.path = item.text()
        self.display_match_set(self.path)


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
    window.setStyleSheet("background-color: rgb(245,247,255);")
    window.show()
    window.raise_()


def main(index_dir):
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow(index_dir)
    setup_window(mw)
    sys.exit(app.exec_())
