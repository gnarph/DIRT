import string

from PyQt4 import QtGui, QtCore

COLUMNS = ['file_name',
           'match_count']

class MainTable(QtGui.QTableWidget):
    """
    Creates a table that self populates
    """

    def _set_initial_column_widths(self):
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 80)
        self.setColumnWidth(4, 80)

    def _set_fonts(self):
        # Header and cell fonts
        font = QtGui.QFont('', 11, QtGui.QFont.Bold)
        self.horizontalHeader().setFont(font)
        cell_font = QtGui.QFont('', 11, QtGui.QFont.AnyStyle)
        self.setFont(cell_font)

    def __init__(self, parent=None):
        super(MainTable, self).__init__(parent)
        self.setColumnCount(5)

        headers = ['Match Title', 'Author(s)', 'Matches',
                   'Match %', 'Path']

        self._set_initial_column_widths()

        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(headers)
        self.setSortingEnabled(True)

        self._set_fonts()

    def populate(self, entries):
        """
        Populates the table with elements
        """
        cols = len(COLUMNS)
        self.setRowCount(len(entries))
        self.setColumnCount(cols)

        # TODO: should use matchsets as entries, not documents
        #       otherwise we don't have the info we need
        for i, entry in enumerate(entries):
            meta = entry.get_metadata()
            for j, col_name in enumerate(COLUMNS):
                item = QtGui.QTableWidgetItem(j)
                uni_val = unicode(meta[col_name])
                item.setText(uni_val)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, j, item)

    def add_data(self, match_file, entries):
        """
        Adds json metadata from a match file
        to a list used to populate the table
        :param match_file: the match file
        :param entries: the list to append to
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, match_file, '')

        match = self.lay_out.m
        match.match_file = fname
        match.setup_matches_list(fname)

        print self.lay_out.m.match_file
        title = 'title'
        author = 'author'
        match_len = 'match length'
        match_percent = 'match percentage'
        path = 'path'
        entries.extend([title, author, match_len, match_percent, path])

