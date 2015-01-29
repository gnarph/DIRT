import codecs
import utilities.file_ops as file_ops
from document_widget import Ui_DocumentPanel
from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QTextCursor

colors = ['#ED1C24', '#F7941D', '#FFF200', '#39B54A', '#00AEEF', '#662D91']


class DocumentUtil():
    """
    DocumentPanel
    Holds and displays two documents in comparison
    """
    # def __init__(self):
    #     self.documentPanel = Ui_DocumentPanel()
    pass


def focus_doc(text_area, file_path, match_file):
    """
    Set the focus document given a file path
    :param dir:
    :return:
    """
    with codecs.open(file_path, 'r', encoding='utf8') as focus:
        text_area.clear()
        highlighted_passage = highlight_matches(focus,
                                    match_file, "alpha_indices",
                                    "alpha_passage")
        text_area.setText(highlighted_passage)



def comp_doc(text_area, file_path, match_file):
    """
    Set the comparison document given a file path
    :param self:
    :param dir:
    :return:
    """
    with codecs.open(file_path, 'r', encoding='utf8') as comparison:
        text_area.clear()
        highlighted_passage = highlight_matches(comparison,
                                                match_file, "beta_indices",
                                                "beta_passage")
        text_area.setText(highlighted_passage)


def highlight_matches(document, match_file, indice, passage):
    with open(match_file) as json_file:
        json_data = file_ops.read_json_utf8(json_file.name)
        json_data = remove_whitespaces(json_data, indice, passage)

        color_suffix = '</font>'
        temp = 0
        test_string = document.read()
        for entry in reversed(json_data['matches']):
            color_prefix = '<font color="' + colors[temp] + '">'

            test_string = insert(test_string, color_suffix, entry[indice][
                1])

            # print entry[indices][1]
            test_string = insert(test_string, color_prefix, entry[indice][
                0])
            # print entry[indices][0]
            temp = (temp+1) % colors.__len__()
            # print indices + ": " + test_string

        return test_string


def remove_whitespaces(json_data, indices, passage):
    """
    Trims the leading/trailing whitespaces and corrects indexes accordingly
    :param json_data:
    :param indices:
    :param passage:
    :return:
    """
    for entry in json_data['matches']:
        if entry[passage].endswith(" "):
            entry[passage] = entry[passage][:-1]
            entry[indices][1] -= 1
        if entry[passage].startswith(" "):
            entry[passage] = entry[passage][1:]
            entry[indices][0] += 1
    return json_data

def insert(original, new, pos):
    """
    Inserts new inside original at pos.
    :param original:
    :param new:
    :param pos:
    :return:
    """
    return original[:pos] + new + original[pos:]