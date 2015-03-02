from PyQt4 import QtGui, QtCore
from dirtgui.main_frame import MainFrame
from dirtgui.main_table import MainTable
from models.match_set_index import MatchSetIndex
import document_util.document_match_util as dmu


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
        self.f_frame.grid.navi_button.clicked.connect(self.prev_match)

        # previous_button = QtGui.QPushButton()
        # previous_button.setText('Previous')
        # previous_button.setMinimumHeight(40)
        # previous_button.clicked.connect(self.prev_match)
        # self.f_frame.grid.addWidget(previous_button, 15, 0, 10, 0)

        self.m_frame = MainFrame(self, 'MATCH')
        match_doc_area = self.m_frame.grid.textEdit

        # next_button = QtGui.QPushButton()
        # next_button.setText('Next')
        # next_button.clicked.connect(self.next_match)
        # self.m_frame.grid.addWidget(next_button, 15, 0 , 10, 0)

        self.m_frame.grid.navi_button.clicked.connect(self.prev_match)

    def _setup_result_table_frame(self):
        self.results_table = MainTable()
        self.results_table.cellDoubleClicked.connect(self.click_display)
        self.results_table.sortByColumn(2)

        table_label = QtGui.QLabel('RESULTS TABLE')
        table_label.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        table_label.setAlignment(QtCore.Qt.AlignCenter)

        # total_match = MatchSetIndex.get_matched_document_count(focus)
        # total_match_label = QtGui.QLabel("Results Found: %d") % (total_match)

        # navigation_bar = QtGui.QHBoxLayout()
        #
        # previous_button = QtGui.QPushButton()
        # previous_button.setText('Previous')
        # previous_button.clicked.connect(self.prev_match)
        # navigation_bar.addWidget(previous_button)
        #
        # next_button = QtGui.QPushButton()
        # next_button.setText('Next')
        # next_button.clicked.connect(self.next_match)
        # navigation_bar.addWidget(next_button)

        vbox = QtGui.QVBoxLayout()
        # vbox.addLayout(navigation_bar)
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

        # TODO: bug - this path is to a document json file
        #       it needs to be the path to a match set json file
        self.display_match_set(self.path)

    def __init__(self, main_window):
        super(MainLayout, self).__init__(main_window)
        self.results_table = None
        self.display_match_set = main_window.display_match_set

        self._setup_comparison_frames()
        table_frame = self._setup_result_table_frame()
        self._setup_splitter_layouts(table_frame)
        self.highlighter = ''

    def next_match(self):
        self.highlighter.highlight_match(1)

    def prev_match(self):
        self.highlighter.highlight_match(-1)
