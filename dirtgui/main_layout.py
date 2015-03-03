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

    scroll_count = 1

    def _setup_comparison_frames(self):
        self.f_frame = MainFrame(self, 'FOCUS')
        self.m_frame = MainFrame(self, 'MATCH')

    def _setup_result_table_frame(self):
        self.results_table = MainTable()
        self.results_table.cellDoubleClicked.connect(self.click_display)
        self.results_table.sortByColumn(2)

        # total_match = MatchSetIndex.get_matched_document_count(focus)
        total_match = 13
        table_label = QtGui.QLabel(('RESULTS FOUND' + ' (%d)') % (total_match))
        table_label.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        table_label.setAlignment(QtCore.Qt.AlignCenter)

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(0, 15, 0, 0)
        vbox.addWidget(table_label)
        vbox.addSpacing(5)
        vbox.addWidget(self.results_table)

        table_frame = QtGui.QFrame(self)
        table_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        table_frame.setLayout(vbox)

        return table_frame

    def _setup_splitter_layouts(self, table_frame):
        hbox = QtGui.QHBoxLayout(self)
        compare_box = QtGui.QVBoxLayout(self)
        compare_box.setContentsMargins(0, 5, 0, 5)

        # Splits focus and match document
        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.f_frame)
        splitter1.addWidget(self.m_frame)

        # # Create navigation frame below splitter 1
        compare_box.addWidget(splitter1)
        # compare_box.addWidget(navi_frame)
        compare_box.setStretch(0, 2)
        compare_frame = QtGui.QFrame(self)
        compare_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        compare_frame.setLayout(compare_box)

        # Splits text comparison from result table
        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(compare_frame)
        splitter2.addWidget(table_frame)
        splitter2.setStretchFactor(0, 1)
        # splitter2.setSizes([0,1])

        # Putting splitter layouts into horizontal layout
        hbox.addWidget(splitter2)
        hbox.setContentsMargins(0, 0, 0, 0)
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
        self.match_scroll(1)

    def prev_match(self):
        self.highlighter.highlight_match(-1)
        self.match_scroll(-1)

    def match_scroll(self, scroll):
        global scroll_count
        if scroll == 1:
            scroll_count += 1
        else:
            scroll_count -= 1
        return scroll_count
