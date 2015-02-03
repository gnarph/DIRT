import utilities.file_ops as file_ops

from PyQt4 import QtCore, QtGui

colors = ['#ED1C24', '#F7941D', '#0000FF', '#39B54A', '#00AEEF', '#662D91']


class DocumentMatchUtil():

    def __init__(self, match_file):
        self.number_of_matches = 0
        self.match_idx = 0
        self.json_data = ""
        self.alpha_list = []
        self.beta_list = []
        self.match_file = match_file
        self.setup_matches_list(self.match_file)

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
            print self.alpha_list
            print self.beta_list
            print self.json_data


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
                                    QtGui.QTextCursor.KeepAnchor, pattern.__len__())
                color.setNamedColor(colors[color_index % colors.__len__()])
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
