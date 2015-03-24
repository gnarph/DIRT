import utilities.file_ops as file_ops

from PyQt4 import QtGui, QtCore
from dirtgui.document_util import document_match_util as match_util


NEXT_TT = u'Move to next match within this document'
PREV_TT = u'Move to prevous match within this document'


class DocumentGrid(QtGui.QGridLayout):
    """
    Creates a grid with Location, Title, Author, and Text READ-only display
    Param: self, title of the layout
    """
    def __init__(self, parent, header, passage_type):
        super(DocumentGrid, self).__init__(parent)

        self.highlighter = ''
        # ------------------------------------------------------
        # Widgets

        # Labels
        header = QtGui.QLabel(header + ' DOCUMENT')
        # HACK
        dummy_location = QtGui.QLabel('Path')
        doc_path = QtGui.QLabel('Path')
        doc_title = QtGui.QLabel('Title')
        #text = QtGui.QLabel('Text :')
        self.passage_type = passage_type

        # Label Fonts
        label_font = QtGui.QFont('', 11, QtGui.QFont.Bold)

        header.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        header.setAlignment(QtCore.Qt.AlignCenter)
        dummy_location.setFont(label_font)
        dummy_location.setAlignment(QtCore.Qt.AlignLeft)
        doc_path.setFont(label_font)
        doc_path.setAlignment(QtCore.Qt.AlignLeft)
        doc_title.setFont(label_font)
        doc_title.setAlignment(QtCore.Qt.AlignLeft)
        #text.setFont(label_font)

        # ------------------------------------------------------
        # Text displays
        self.dummyLocationEdit = QtGui.QTableWidget.locationEdit = QtGui.QLineEdit()
        self.documentPathEdit = QtGui.QTableWidget.titleEdit = QtGui.QLineEdit()
        self.documentTitleEdit = QtGui.QTableWidget.authorEdit = QtGui.QLineEdit()
        self.textEdit = QtGui.QTableWidget.textEdit = QtGui.QTextEdit()

        self.textEdit.setStyleSheet("background-color: rgb(255,255,255);")

        # Text display font
        display_font = QtGui.QFont('', 12)

        self.dummyLocationEdit.setFont(display_font)
        self.documentPathEdit.setFont(display_font)
        self.documentTitleEdit.setFont(display_font)
        self.textEdit.setFont(display_font)

        # Set all text displays to READ-only
        QtGui.QTableWidget.locationEdit.setReadOnly(True)
        QtGui.QTableWidget.titleEdit.setReadOnly(True)
        QtGui.QTableWidget.authorEdit.setReadOnly(True)
        QtGui.QTableWidget.textEdit.setReadOnly(True)

        navigation_bar = QtGui.QHBoxLayout()

        previous_button = QtGui.QPushButton()
        previous_button.setText('Prev')
        previous_button.setToolTip(PREV_TT)
        # previous_button.setMaximumSize(30,50)
        previous_button.clicked.connect(self.prev_match)
        navigation_bar.addWidget(previous_button)

        next_button = QtGui.QPushButton()
        next_button.setText('Next')
        next_button.setToolTip(NEXT_TT)
        # next_button.setMaximumSize(30,50)
        next_button.clicked.connect(self.next_match)
        navigation_bar.addWidget(next_button)
        # Cursor
        #self.textEdit.setTextCursor(QtGui.QTextCursor())

        # ------------------------------------------------------
        # Position on Grid Layout

        # Header
        self.setSpacing(10)
        self.addWidget(header, 0, 1, QtCore.Qt.AlignCenter)
        self.verticalSpacing()

        # Path
        # self.addWidget(dummy_location, 1, 0)
        # self.addWidget(QtGui.QTableWidget.dummyLocationEdit, 1, 1)

        # Title
        self.addWidget(doc_path, 2, 0)
        self.addWidget(QtGui.QTableWidget.titleEdit, 2, 1)

        # Author
        self.addWidget(doc_title, 3, 0)
        self.addWidget(QtGui.QTableWidget.authorEdit, 3, 1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        previous_button.setSizePolicy(sizePolicy)
        previous_button.setMaximumWidth(35)
        self.addWidget(previous_button, 4, 0, 1, 1, QtCore.Qt.AlignRight)

        next_button.setSizePolicy(sizePolicy)
        next_button.setMaximumWidth(35)
        self.addWidget(next_button, 5, 0, 1, 1, QtCore.Qt.AlignRight)

        # self.addWidget(text, 4, 0)
        self.addWidget(QtGui.QTableWidget.textEdit, 4, 1, 3, 1)

        self.setRowStretch(3, 5)

        self.file_path = ''
        self.match_file = ''

    def set_document(self, file_path):
        """

        :param file_path:
        :return:
        """
        passage = file_ops.read_utf8(file_path)

        self.textEdit.clear()
        self.textEdit.setText(passage)

    def highlight_document(self, match_set, passage):
        """

        :param match_set:
        :param passage:
        :return:
        """
        text_area = self.textEdit
        cursor = text_area.textCursor()
        match_util.highlight_document(text_area, cursor, match_set, passage)

    def next_match(self):
        self.highlighter.highlight_match(1, self.passage_type)

    def prev_match(self):
        self.highlighter.highlight_match(-1, self.passage_type)
