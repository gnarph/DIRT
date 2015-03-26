from PyQt4 import QtGui, QtCore

HEADER = ['Match Name',
          'Focus %',
          'Match %',
          'Match Count']

COLUMNS = ['file_name',
           'alpha_match_pct',
           'beta_match_pct',
           'match_count']

COLUMN_TT = [u'Name of file',
             u'Percentage of focus that is a match',
             u'Percentage of other document that is a match',
             u'Number of matching passages']


class NumericalTableWidgetItem(QtGui.QTableWidgetItem):
    def __lt__(self, other):
        if isinstance(other, QtGui.QTableWidgetItem):
            my_value, my_ok = self.data(QtCore.Qt.EditRole).toFloat()
            other_value, other_ok = other.data(QtCore.Qt.EditRole).toFloat()

            if my_ok and other_ok:
                return my_value < other_value

        return super(NumericalTableWidgetItem, self).__lt__(other)


class ResultsTable(QtGui.QTableWidget):
    """
    Creates a table that self populates
    """

    def _set_header_tooltips(self):
        for i in xrange(len(COLUMN_TT)):
            header_item = self.horizontalHeaderItem(i)
            tool_tip = COLUMN_TT[i]
            header_item.setToolTip(tool_tip)

    def _set_initial_column_widths(self):
        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 130)
        self.setColumnWidth(2, 130)
        self.setColumnWidth(3, 130)

    def _set_fonts(self):
        # Header and cell fonts
        font = QtGui.QFont('', 11, QtGui.QFont.Bold)
        self.horizontalHeader().setFont(font)
        cell_font = QtGui.QFont('', 11, QtGui.QFont.AnyStyle)
        self.setFont(cell_font)

    def __init__(self, parent=None):
        super(ResultsTable, self).__init__(parent)
        self.setColumnCount(len(COLUMNS))
        self._set_initial_column_widths()
        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(HEADER)
        self.setSortingEnabled(True)

        self._set_fonts()
        self._set_header_tooltips()

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
                uni_val = unicode(meta[col_name])
                if j >= 1:
                    # Numerical columns
                    # TODO HACK
                    item = NumericalTableWidgetItem(j)
                    item.setData(QtCore.Qt.EditRole, QtCore.QVariant(float(uni_val)))
                else:
                    item = QtGui.QTableWidgetItem(j)
                item.setText(uni_val)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, j, item)
