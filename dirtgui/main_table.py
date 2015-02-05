import string
from PyQt4 import QtGui, QtCore


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

        # Code to populate table

        self.matches = []
        self.entries = []
        self.match_list(fname, self.matches)
        self.datalist(self.matches, self.entries)
        self.populate(self.entries)

    def populate(self, entries):
        """
        Populates the table with elements
        """

        # # Populates table with alphabetical lettering
        # self.setRowCount(10)
        #
        # for i in range(10):
        #     for j,l in enumerate(string.letters[:5]):
        #         item = QtGui.QTableWidgetItem(l)
        #         # Line below locks the item in the cells
        #         item.setFlags(QtCore.Qt.ItemIsEnabled)
        #         self.setItem(i, j, item)

        # Populates table using a list by column then row

        # entries = []
        # with open('data') as input:
        #     for line in input:
        #         entries.append(line.strip().split('\t'))

        self.setRowCount(len(entries))
        # self.setColumnCount(len(entries[0]))

        for i, row in enumerate(entries):
            for j, col in range(5):
                item = QtGui.QTableWidgetItem(col)
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

    def match_list(self, focus, matches):
        """
        Retrieves all matches of the focus document
        and appends them to a list
        :param focus: focus document name
        :param matches: list to store the matches
        """
        match = self.lay_out.m
        match.match_file = fname
        match.setup_matches_list(focus)

        matches.extend([])


    def data_list(self, matches, entries):
        """
        Appends the metadata from all matches to a list
        :param matches: List of all matches
        :param entries: List of metadata
        """

        for match in len(matches):
            self.add_data(match, entries)