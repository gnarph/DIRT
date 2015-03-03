import utilities.file_ops as file_ops
import models.match_set_index as match_set_index

from PyQt4 import QtCore, QtGui
from operator import itemgetter

colors = ['#ED1C24', '#F7941D', '#0000FF', '#39B54A', '#00AEEF', '#662D91']


class Highlighter():

    def __init__(self, focus, match, match_set):
        self.focus_text_area = focus
        self.match_text_area = match
        self.ms = match_set
        self.number_of_matches = len(match_set.get_indices())
        self.match_idx = self.number_of_matches - 1
        if self.number_of_matches > 0:
            self.alpha_array = sorted(match_set.get_indices(),
                                      key=itemgetter(0))
            self.beta_array = sorted(match_set.get_indices(),
                                     key=itemgetter(1))

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

    def highlight_match(self, direction, passage_type):
        number_of_matches = len(self.alpha_array)
        if number_of_matches != 0:
            if passage_type == 'alpha_passage':
                array = self.alpha_array
            else:
                array = self.beta_array
            prev_match_idx = self.match_idx

            focus_pair = array[prev_match_idx][0]
            focus_cursor_pos = focus_pair[0]
            length = focus_pair[1] - focus_pair[0]
            remove_match_highlight(self.focus_text_area, focus_cursor_pos,
                                   length)

            match_pair = array[prev_match_idx][1]
            comp_cursor_pos = match_pair[0]
            length = match_pair[1] - match_pair[0]
            remove_match_highlight(self.match_text_area, comp_cursor_pos,
                                   length)

            self.match_idx = (self.match_idx + direction) % number_of_matches
            match_idx = self.match_idx

            current_focus_pair = array[match_idx][0]
            focus_cursor_pos = current_focus_pair[0]
            length = current_focus_pair[1] - current_focus_pair[0]
            move_cursor(self.focus_text_area, focus_cursor_pos, length)

            current_match_pair = array[match_idx][1]
            comp_cursor_pos = current_match_pair[0]
            length = current_match_pair[1] - current_match_pair[0]
            move_cursor(self.match_text_area, comp_cursor_pos, length)


def highlight_document(text_area, cursor, match_set, passage):
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

    if passage == 'alpha':
        passages = match_set.alpha_passages()
    else:
        passages = match_set.beta_passages()

    for entry in passages:
        pattern = entry
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
            text_format.setForeground(QtGui.QBrush(color))
            text_format.setBackground(QtGui.QBrush("black"))
            cursor.mergeCharFormat(text_format)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(text_area.toPlainText(), pos)
        color_index += 1


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
    if entry[passage].endswith("\n"):
        entry[passage] = entry[passage][:-2]
        entry[indices][1] -= 2


def move_cursor(doc, pos, length):
    """

    :param doc:
    :param pos:
    :param length:
    :return:
    """
    color = QtGui.QColor()
    color.setNamedColor("#FFF000")
    text_format = QtGui.QTextCharFormat()
    text_format.setBackground(QtGui.QBrush(color))
    text_cursor = doc.textCursor()
    text_cursor.setPosition(pos)
    text_cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                             QtGui.QTextCursor.KeepAnchor, length)
    text_cursor.mergeCharFormat(text_format)
    doc.setTextCursor(text_cursor)

    cursor = doc.cursorRect()
    cursor_top = cursor.top()
    vbar = doc.verticalScrollBar()
    vbar.setSliderPosition(vbar.value() + cursor_top - length*2)
    doc.ensureCursorVisible()


def remove_match_highlight(doc, pos, length):
    """

    :param doc:
    :param pos:
    :param length:
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


def clear_highlight(doc):
    """

    :param doc:
    :param pos:
    :param length:
    :return:
    """
    color = QtGui.QColor()
    color.setNamedColor("#FFFFFF")
    text_format = QtGui.QTextCharFormat()
    text_format.setBackground(QtGui.QBrush(color))
    text_cursor = doc.textCursor()
    # Remove any highlighted text
    text_cursor.setPosition(0)
    text_cursor.movePosition(QtGui.QTextCursor.End,
                             QtGui.QTextCursor.KeepAnchor)
    text_cursor.setCharFormat(text_format)
    doc.setTextCursor(text_cursor)
    # Return cursor position to start of document
    text_cursor.setPosition(0)
    text_cursor.movePosition(QtGui.QTextCursor.Start,
                             QtGui.QTextCursor.MoveAnchor)
    text_cursor.setCharFormat(text_format)
    doc.setTextCursor(text_cursor)
    doc.ensureCursorVisible()