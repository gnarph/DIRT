

class Document(object):
    """
    Class for representing a document in memory
    """

    def __init__(self, file_name, body, metadata=None):
        """
        :param file_name: name of file document represents
        :param body: textual body of document (unicode)
        :param metadata: dict of metadata
        """
        self.file_name = file_name
        self.body = body
        self.metadata = metadata if metadata else {}

    def clone(self):
        return Document(self.file_name,
                        self.body,
                        self.metadata)

    def to_dict(self):
        return {'file_name': self.file_name,
                'body': self.body,
                'metadata': self.metadata,
                }

    def __eq__(self, other):
        if self.file_name != other.file_name:
            return False
        if self.metadata != other.metadata:
            return False
        if self.body != other.body:
            return False
        return True
