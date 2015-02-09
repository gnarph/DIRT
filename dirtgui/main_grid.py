import utilities.file_ops as file_ops

from PyQt4 import QtGui, QtCore
from dirtgui.document_util import document_match_util as match_util


class MainGrid(QtGui.QGridLayout):
    """
    Creates a grid with Location, Title, Author, and Text READ-only display
    Param: self, title of the layout
    """
    def __init__(self, parent, header, passage_type):
        super(MainGrid, self).__init__(parent)

        # ------------------------------------------------------
        # Widgets

        # Labels
        header = QtGui.QLabel(header)
        location = QtGui.QLabel('Path :')
        title = QtGui.QLabel('Title :')
        author = QtGui.QLabel('Author :')
        #text = QtGui.QLabel('Text :')
        self.passage_type = passage_type

        # Label Fonts
        label_font = QtGui.QFont('', 11, QtGui.QFont.Bold)

        header.setFont(QtGui.QFont('', 11.5, QtGui.QFont.Bold))
        header.setAlignment(QtCore.Qt.AlignCenter)
        location.setFont(label_font)
        location.setAlignment(QtCore.Qt.AlignRight)
        title.setFont(label_font)
        title.setAlignment(QtCore.Qt.AlignRight)
        author.setFont(label_font)
        author.setAlignment(QtCore.Qt.AlignRight)
        #text.setFont(label_font)

        # ------------------------------------------------------
        # Text displays
        self.locationEdit = QtGui.QTableWidget.locationEdit = QtGui.QLineEdit()
        self.titleEdit = QtGui.QTableWidget.titleEdit = QtGui.QLineEdit()
        self.authorEdit = QtGui.QTableWidget.authorEdit = QtGui.QLineEdit()
        self.textEdit = QtGui.QTableWidget.textEdit = QtGui.QTextEdit()

        self.textEdit.setStyleSheet("background-color: rgb(255,255,255);")

        # Text display font
        display_font = QtGui.QFont('', 12)

        self.locationEdit.setFont(display_font)
        self.titleEdit.setFont(display_font)
        self.authorEdit.setFont(display_font)
        self.textEdit.setFont(display_font)

        # Set all text displays to READ-only
        QtGui.QTableWidget.locationEdit.setReadOnly(True)
        QtGui.QTableWidget.titleEdit.setReadOnly(True)
        QtGui.QTableWidget.authorEdit.setReadOnly(True)
        QtGui.QTableWidget.textEdit.setReadOnly(True)

        # Cursor
        #self.textEdit.setTextCursor(QtGui.QTextCursor())

        # ------------------------------------------------------
        # Position on Grid Layout

        # Header
        self.setSpacing(10)
        self.addWidget(header, 0, 1)

        # Path
        self.addWidget(location, 1, 0)
        self.addWidget(QtGui.QTableWidget.locationEdit, 1, 1)

        # Title
        self.addWidget(title, 2, 0)
        self.addWidget(QtGui.QTableWidget.titleEdit, 2, 1)

        # Author
        self.addWidget(author, 3, 0)
        self.addWidget(QtGui.QTableWidget.authorEdit, 3, 1)

        # Text
        #self.addWidget(text, 4, 0)
        self.addWidget(QtGui.QTableWidget.textEdit, 4, 0, 10, -1)

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
