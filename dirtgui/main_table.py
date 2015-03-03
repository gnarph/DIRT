import string

from PyQt4 import QtGui, QtCore
from models.match_set_index import MatchSetIndex
from models.match_set import MatchSet

HEADER = ['Match Name',
          'Author(s)',
          'Focus Common %',
          'Match Common %',
          'Match Count']

COLUMNS = ['file_name',
           'edition',
           'alpha_match_pct',
           'beta_match_pct',
           'match_count']


class MainTable(QtGui.QTableWidget):
    """
    Creates a table that self populates
    """

    def _set_initial_column_widths(self):
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 130)
        self.setColumnWidth(3, 130)
        self.setColumnWidth(4, 100)

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
        self.setHorizontalHeaderLabels(HEADER)
        self.setSortingEnabled(True)

        self._set_fonts()

    def populate(self, focus_name, msi):
        """
        Populates the table with metadata
        """

        match_set_list = msi.get_all_match_sets(focus_name=focus_name)
        cols = len(COLUMNS)
        self.setRowCount(len(match_set_list))
        self.setColumnCount(cols)

        # TODO: should use matchsets as entries, not documents
        #       otherwise we don't have the info we need
        for i, match_set in enumerate(match_set_list):
            meta = match_set.get_beta_metadata()
            for j, col_name in enumerate(COLUMNS):
                item = QtGui.QTableWidgetItem(j)
                uni_val = unicode(meta[col_name])
                item.setText(uni_val)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, j, item)

    def _get_matchset_list(self, focus_doc, output_dir):
        """
        List of all matches found to the focus
        :param match_file: the match file
        :param entries: the list to append to
        """
        msi = MatchSetIndex(output_dir)
        self.focus = str(focus_doc)
        matchset_list = msi.get_all_match_sets(self.focus)
        return matchset_list

    def _get_sorted_metadata(self, metadata):
        sorted_metadata = []
        title = metadata.get('title')
        author = metadata.get('author')
        match_len = metadata.get('match_len')
        match_percent = metadata.get('match_percent')
        path = metadata.get('path')
        sorted_metadata.extend([title, author, match_len, match_percent, path])
        return sorted_metadata