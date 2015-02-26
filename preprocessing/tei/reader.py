import preprocessing.tei.document as tei_document


class TEIReader(object):
    """
    Class for reading useful information from a TEI encoded
    xml file
    """

    def __init__(self, file_name):
        """
        :param file_name: Name of TEI encoded xml file
        """
        self.file_name = file_name

    def read(self):
        """
        Read TEI xml document into a more useful form
        :return: unicode text body, metadata dictionary
        """
        doc = tei_document.TEIDocument(self.file_name)
        data_dict = doc.get_data()
        body = data_dict['body']
        del data_dict['body']

        return body, data_dict
