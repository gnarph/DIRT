from utilities import file_reading


class Document(object):
    """
    Class for representing a document in memory
    """

    def __init__(self, file_name, pre_file_name='', metadata=None):
        """

        :param pre_file_name:
        :param file_name: name of file document represents
        :param metadata: dict of metadata
        """
        self.file_name = file_name
        self.pre_file_name = pre_file_name
        self.metadata = metadata if metadata else {}

    @property
    def body(self):
        return file_reading.read_utf8(self.file_name)

    @property
    def pre_body(self):
        return file_reading.read_utf8(self.pre_file_name)

    def clone(self):
        return Document(file_name=self.file_name,
                        metadata=self.metadata,
                        pre_file_name=self.pre_file_name)

    def to_dict(self):
        return {'file_name': self.file_name,
                'metadata': self.metadata,
                'pre_file_name': self.pre_file_name,
                }

    def __eq__(self, other):
        if self.file_name != other.file_name:
            return False
        if self.metadata != other.metadata:
            return False
        if self.pre_file_name != other.pre_file_name:
            return False
        return True
