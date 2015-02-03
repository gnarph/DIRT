import codecs


class DocumentUtil():

    def __init__(self):
        pass


def open_doc(text_area, file_path):
    """
    Opens a document and display it in a text area
    :param text_area:
    :param file_path:
    :return:
    """
    with codecs.open(file_path, 'r', encoding='utf8') as document:
        text_area.clear()
        text_area.setText(document.read())