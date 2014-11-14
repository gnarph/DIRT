from utilities import file_ops


class Document(object):
    """
    Class for representing a document in memory
    """

    def __init__(self, file_name, raw_file_name='',
                 pre_file_name='', metadata=None):
        """

        :param pre_file_name:
        :param file_name: name of file document represents
        :param metadata: dict of metadata
        """
        self.file_name = file_name
        self.raw_file_name = raw_file_name
        self.pre_file_name = pre_file_name
        self.metadata = metadata if metadata else {}

    @staticmethod
    def from_json(file_name):
        data = file_ops.read_json_utf8(file_name)
        return Document(file_name=data['file_name'],
                        raw_file_name=data['raw_file_name'],
                        metadata=data['metadata'],
                        pre_file_name=data['pre_file_name'])

    @property
    def body(self):
        return file_ops.read_utf8(self.file_name)

    @property
    def raw_body(self):
        return file_ops.read_json_utf8(self.raw_file_name)

    @property
    def pre_body(self):
        return file_ops.read_utf8(self.pre_file_name)

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
