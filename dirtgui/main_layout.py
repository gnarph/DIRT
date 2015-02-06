from PyQt4 import QtGui, QtCore
from dirtgui.document_util import document_match_util as match_util
from dirtgui.main_frame import MainFrame
from dirtgui.main_table import MainTable


class MainLayout(QtGui.QWidget):
    """
    Splitter layout that separates frames
    and allows to adjust the size relatively
    then puts everything in a horizontal layout
    Theme: 'cleanlooks'
    """

    def _setup_comparison_frames(self):
        self.f_frame = MainFrame(self, 'FOCUS')
        focus_doc_area = self.f_frame.grid.textEdit
        self.m_frame = MainFrame(self, 'MATCH')
        match_doc_area = self.m_frame.grid.textEdit
        self.m = match_util.DocumentMatchUtil(focus_doc_area,
                                              match_doc_area, '')

    def _setup_result_table_frame(self):
        self.results_table = MainTable()
        self.results_table.cellDoubleClicked.connect(self.click_display)
        table_label = QtGui.QLabel('RESULTS TABLE')
        table_label.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        table_label.setAlignment(QtCore.Qt.AlignCenter)

        navigation_bar = QtGui.QHBoxLayout()

        previous_button = QtGui.QPushButton()
        previous_button.setText('Previous')
        previous_button.clicked.connect(self.m.prev_match)
        navigation_bar.addWidget(previous_button)

        next_button = QtGui.QPushButton()
        next_button.setText('Next')
        next_button.clicked.connect(self.m.next_match)
        navigation_bar.addWidget(next_button)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(navigation_bar)
        vbox.addWidget(table_label)
        vbox.addWidget(self.results_table)

        # vbox.setAlignment(QtCore.Qt.AlignCenter)
        table_frame = QtGui.QFrame(self)
        table_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        table_frame.setLayout(vbox)
        return table_frame

    def _setup_splitter_layouts(self, table_frame):
        hbox = QtGui.QHBoxLayout(self)

        # Splits focus and match document
        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.f_frame)
        splitter1.addWidget(self.m_frame)

        # Splits text comparison from result table
        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(table_frame)

        # Putting splitter layouts into horizontal layout
        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))

    def click_display(self, row, column):
        """
        When clicked, displays the match document in the text box
        """

        print("Row %d and Column %d was clicked" % (row, column))
        item = self.results_table.item(row, 4)
        self.path = item.text()
        print self.path

        self.display_match_set(self.path)

    def __init__(self, parent):
        super(MainLayout, self).__init__(parent)
        self.results_table = None

        self._setup_comparison_frames()
        table_frame = self._setup_result_table_frame()
        self._setup_splitter_layouts(table_frame)