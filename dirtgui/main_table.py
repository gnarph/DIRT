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
        self.populate()

        headers = ['Match Title', 'Author(s)', 'Matches',
                   'Match %', 'Location']

        self._set_initial_column_widths()

        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(headers)
        self.setSortingEnabled(True)

        self._set_fonts()

    def populate(self):
        """
        Populates the table with elements
        """

        # Populates table with alphabetical lettering
        self.setRowCount(10)

        for i in range(10):
            for j,l in enumerate(string.letters[:5]):
                item = QtGui.QTableWidgetItem(l)
                # Line below locks the item in the cells
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, j, item)

        # Populates table using a list by column then row
        """
        entries = []
        with open('data') as input:
            for line in input:
                entries.append(line.strip().split('\t'))

        tableWidget.setRowCount(len(entries))
        tableWidget.setColumnCount(len(entries[0]))

        for i, row in enumerate(entries):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                tableWidget.setItem(i, j, item)
        """