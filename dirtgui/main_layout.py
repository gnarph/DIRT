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

        self.m_frame = MainFrame(self, 'MATCH')
        match_doc_area = self.m_frame.grid.textEdit


    def _setup_result_table_frame(self):
        self.results_table = MainTable()
        self.results_table.cellDoubleClicked.connect(self.click_display)
        self.results_table.sortByColumn(2)

        table_label = QtGui.QLabel('RESULTS TABLE')
        table_label.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        table_label.setAlignment(QtCore.Qt.AlignCenter)

        # total_match = MatchSetIndex.get_matched_document_count(focus)
        # total_match_label = QtGui.QLabel("Results Found: %d") % (total_match)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(table_label)
        vbox.addWidget(self.results_table)

        table_frame = QtGui.QFrame(self)
        table_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        table_frame.setLayout(vbox)

        return table_frame

    def _setup_navi_frame(self):
        navi_bar = QtGui.QGridLayout()

        previous_button = self._navi_button('Previous')
        previous_button.clicked.connect(self.prev_match)
        navi_bar.addWidget(previous_button, 0, 0, 0, 2, QtCore.Qt.AlignCenter)


        next_button = self._navi_button('Next')
        next_button.clicked.connect(self.next_match)
        navi_bar.addWidget(next_button, 0, 4, 0, 2, QtCore.Qt.AlignCenter)

        navi_frame = QtGui.QFrame(self)
        navi_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        navi_frame.setLayout(navi_bar)

        return navi_frame

    def _navi_button(self, button):
        navi_button = QtGui.QPushButton()
        navi_button.setText(button)
        navi_button.setMinimumSize(300, 37)
        label_font = QtGui.QFont('', 11, QtGui.QFont.Bold)
        navi_button.setFont(label_font)
        return navi_button

    def _setup_splitter_layouts(self, table_frame, navi_frame):
        hbox = QtGui.QHBoxLayout(self)
        compare_box = QtGui.QVBoxLayout(self)

        # Splits focus and match document
        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.f_frame)
        splitter1.addWidget(self.m_frame)

        # Create navigation frame below splitter 1
        compare_box.addWidget(splitter1)
        compare_box.addWidget(navi_frame)
        compare_box.setStretch(0, 2)
        compare_frame = QtGui.QFrame(self)
        compare_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        compare_frame.setLayout(compare_box)

        # Splits text comparison from result table
        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(compare_frame)
        splitter2.addWidget(table_frame)
        splitter2.setSizes([2,1])
        splitter2.setStretchFactor(0, 1)

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
        navi_frame = self._setup_navi_frame()
        self._setup_splitter_layouts(table_frame, navi_frame)
        self.highlighter = ''

    def next_match(self):
        self.highlighter.highlight_match(1)

    def prev_match(self):
        self.highlighter.highlight_match(-1)
