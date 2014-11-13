import models.document
import preprocessing.tei.document as tei_document


class TEIReader(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        """
        Read TEI xml document into a more useful form
        :return: models.document for file
        """
        # TODO: is this module necessary?
        doc = tei_document.TEIDocument(self.file_name)
        data_dict = doc.get_data()
        body = data_dict['body']
        del data_dict['body']

        return models.document.Document(file_name=self.file_name,
                                        body=body,
                                        metadata=data_dict)
