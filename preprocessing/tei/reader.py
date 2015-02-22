import preprocessing.tei.document as tei_document


class TEIReader(object):

    def __init__(self, file_name):
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
