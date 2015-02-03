import codecs
import utilities.file_ops as file_ops

from PyQt4 import QtCore, QtGui

colors = ['#ED1C24', '#F7941D', '#0000FF', '#39B54A', '#00AEEF', '#662D91']


class DocumentMatchUtil():

    def __init__(self, focus, match, match_file):
        self.focus_doc = focus
        self.match_doc = match
        self.number_of_matches = 0
        self.match_idx = 0
        self.json_data = ''
        self.alpha_list = []
        self.beta_list = []
        self.match_file = match_file
        # self.setup_matches_list(self.match_file)

    def setup_matches_list(self, match_file):
        with open(match_file) as json_file:
            self.json_data = file_ops.read_json_utf8(json_file.name)
            trim_sentences(self.json_data)
            self.number_of_matches = len(self.json_data['matches'])
            for i in range(0, self.number_of_matches):
                self.alpha_list.append(self.json_data['matches'][i][
                    'alpha_indices'][0])
                self.beta_list.append(self.json_data['matches'][i][
                    'beta_indices'][0])

    def next_match(self):
        """
        Moves cursor and scrolls view of focus and comparison text area to
        next match
        :return:
        """
        self.highlight_match(1)

    def prev_match(self):
        """
        Moves cursor and scrolls view of focus and comparison text area to
        previous match
        :return:
        """
        self.highlight_match(-1)

    def highlight_match(self, direction):
        prev_match_idx = self.match_idx
        # focus_cursor = self.doc_focus.textCursor()
        focus_cursor_pos = self.alpha_list[prev_match_idx]
        length = len(self.json_data['matches'][prev_match_idx][
            'alpha_passage'])
        remove_highlight(self.focus_doc, focus_cursor_pos, length)
        # comp_cursor = self.doc_comparison.textCursor()
        comp_cursor_pos = self.beta_list[prev_match_idx]
        length = len(self.json_data['matches'][prev_match_idx][
            'beta_passage'])
        remove_highlight(self.match_doc, comp_cursor_pos, length)

        self.match_idx = (self.match_idx + direction) % self.number_of_matches
        match_idx = self.match_idx
        focus_cursor_pos = self.alpha_list[match_idx]
        length = len(self.json_data['matches'][match_idx][
            'alpha_passage'])
        move_cursor(self.focus_doc, focus_cursor_pos, length)
        comp_cursor_pos = self.beta_list[match_idx]
        length = len(self.json_data['matches'][match_idx][
            'beta_passage'])
        move_cursor(self.match_doc, comp_cursor_pos, length)


def highlight_matches(text_area, cursor, match_file, passage):
    """

    :param text_area:
    :param cursor:
    :param match_file:
    :param passage: alpha or beta
    :return:
    """
    text_format = QtGui.QTextCharFormat()
    color = QtGui.QColor()
    color_index = 0
    with open(match_file) as json_file:
        json_data = file_ops.read_json_utf8(json_file.name)

        for entry in json_data['matches']:
            pattern = entry[passage]

            regex = QtCore.QRegExp(pattern)

            pos = 0
            index = regex.indexIn(text_area.toPlainText(), pos)
            while index != -1:
                # Select the matched text and apply the desired format
                cursor.setPosition(index)
                cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                                    QtGui.QTextCursor.KeepAnchor,
                                    len(pattern))
                color.setNamedColor(colors[color_index % len(colors)])
                color_index += 1
                text_format.setForeground(QtGui.QBrush(color))
                cursor.mergeCharFormat(text_format)
                # Move to the next match
                pos = index + regex.matchedLength()
                index = regex.indexIn(text_area.toPlainText(), pos)


def trim_sentences(match_file):
    """
    Trims the leading/trailing whitespaces of sentences in a match file
    :param match_file:
    :return:
    """
    for entry in match_file['matches']:
        trim_whitespace(entry, "alpha_indices", "alpha_passage")
        trim_whitespace(entry, "beta_indices", "alpha_passage")
    return match_file


def trim_whitespace(entry, indices, passage):
    """
    Trims a sentence of leading/trailing whitespaces and updates indices
    :param entry:
    :param indices:
    :param passage:
    :return:
    """
    if entry[passage].endswith(" "):
        entry[passage] = entry[passage][:-1]
        entry[indices][1] -= 1
    if entry[passage].startswith(" "):
        entry[passage] = entry[passage][1:]
        entry[indices][0] += 1


def move_cursor(doc, pos, length):
    """
    Moves cursor
    :param doc: QTextEdit
    :param pos: int
    :param length: int
    :return:
    """
    color = QtGui.QColor()
    color.setNamedColor("#FFF000")
    text_format = QtGui.QTextCharFormat()
    text_format.setBackground(QtGui.QBrush(color))
    text_cursor = doc.textCursor()
    if pos == 0:
        doc.moveCursor(QtGui.QTextCursor.Start, QtGui.QTextCursor.KeepAnchor)
    text_cursor.setPosition(pos)
    text_cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                             QtGui.QTextCursor.KeepAnchor, length)
    text_cursor.mergeCharFormat(text_format)
    doc.setTextCursor(text_cursor)

    doc.ensureCursorVisible()
    doc.clearFocus()


def remove_highlight(doc, pos, length):
    """
    Moves cursor to remove highlight
    :param doc:
    :param pos:
    :return:
    """
    color = QtGui.QColor()
    color.setNamedColor("#FFFFFF")
    text_format = QtGui.QTextCharFormat()
    text_format.setBackground(QtGui.QBrush(color))
    text_cursor = doc.textCursor()
    text_cursor.setPosition(pos)
    text_cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                             QtGui.QTextCursor.KeepAnchor, length)
    text_cursor.mergeCharFormat(text_format)
    doc.setTextCursor(text_cursor)
    doc.ensureCursorVisible()


def find_string(self):
    s = str(self.lineEdit.displayText())
    length = len(s)
    with codecs.open(self.focus, 'r', encoding='utf8') as focus:
        index = focus.read().lower().index(s)
        print s
        print index
        index = focus.read().index(s)

