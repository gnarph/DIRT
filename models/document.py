

class Document(object):
    """
    Class for representing a document in memory
    """

    def __init__(self, file_name, body, metadata=None, pre_file_name=''):
        """

        :param pre_file_name:
        :param file_name: name of file document represents
        :param body: textual body of document (unicode)
        :param metadata: dict of metadata
        """
        self.file_name = file_name
        self.body = body
        self.metadata = metadata if metadata else {}
        self.pre_file_name = pre_file_name

    def clone(self):
        return Document(self.file_name,
                        self.body,
                        self.metadata,
                        self.pre_file_name)

    def to_dict(self):
        return {'file_name': self.file_name,
                'body': self.body,
                'metadata': self.metadata,
                'pre_file_name': self.pre_file_name,
                }

    def __eq__(self, other):
        if self.file_name != other.file_name:
            return False
        if self.metadata != other.metadata:
            return False
        if self.body != other.body:
            return False
        if self.pre_file_name != other.pre_file_name:
            return False
        return True
