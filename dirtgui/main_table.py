import string

from PyQt4 import QtGui, QtCore
from models.match_set_index import MatchSetIndex
from models.match_set import MatchSet

COLUMNS = ['Match Title', 'Author(s)', 'Matches',
           'Match %', 'Path']

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
        self._set_initial_column_widths()
        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(COLUMNS)
        self.setSortingEnabled(True)

        self._set_fonts()

    def populate(self, focus):
        """
        Populates the table with metadata
        """

        match_list = self._get_match_list(focus)
        cols = len(COLUMNS)
        self.setRowCount(len(match_list))
        self.setColumnCount(cols)

        # TODO: should use matchsets as entries, not documents
        #       otherwise we don't have the info we need
        for i, match in enumerate(match_list):
            meta = match.get_metadata()
            for j, col_name in enumerate(COLUMNS):
                item = QtGui.QTableWidgetItem(j)
                uni_val = unicode(meta[col_name])
                item.setText(uni_val)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, j, item)

    def _get_match_list(self, focus_doc):
        """
        List of all matches found to the focus
        :param match_file: the match file
        :param entries: the list to append to
        """
        msi = MatchSetIndex()
        self.focus = focus_doc
        match_list = msi.get_all_matched_documents(self.focus)
        return match_list

    def _get_sorted_metadata(self, metadata):
        sorted_metadata = []
        title = metadata.get('title')
        author = metadata.get('author')
        match_len = metadata.get('match_len')
        match_percent = metadata.get('match_percent')
        path = metadata.get('path')
        sorted_metadata.extend([title, author, match_len, match_percent, path])
        return sorted_metadata