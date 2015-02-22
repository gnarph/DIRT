from collections import defaultdict

from utilities import file_ops


class InvalidDocumentException(BaseException):
    pass


def error_handler(fn):
    def wrapped(*args, **kwargs):
        try:
            val = fn(*args, **kwargs)
        except (file_ops.DIRTFileException, KeyError) as e:
            template = u'Error {err} in {func_name} with args {args},{kwargs}'
            msg = template.format(err=str(e),
                                  func_name=str(fn),
                                  args=args,
                                  kwargs=kwargs)
            raise InvalidDocumentException(msg)
        return val
    return wrapped


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
    @error_handler
    def from_json(file_name):
        if not file_name.endswith('.json'):
            template = 'Need json file, got {}'
            message = template.format(file_name)
            raise InvalidDocumentException(message)
        data = file_ops.read_json_utf8(file_name)
        return Document(file_name=file_name,
                        raw_file_name=data['raw_file_name'],
                        metadata=data['metadata'],
                        pre_file_name=data['pre_file_name'])

    @property
    def raw_body(self):
        """
        Get the body of the file
        """
        return file_ops.read_utf8(self.raw_file_name)

    @property
    def pre_body(self):
        """
        Get the preprocessed body of the file
        """
        return file_ops.read_utf8(self.pre_file_name)

    def clone(self):
        return Document(file_name=self.file_name,
                        metadata=self.metadata,
                        pre_file_name=self.pre_file_name,
                        raw_file_name=self.raw_file_name)

    def to_dict(self):
        """
        Covert to dictionary representation
        :return: dict
        """
        return {'file_name': self.file_name,
                'raw_file_name': self.raw_file_name,
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
        if self.raw_file_name != other.raw_file_name:
            return False
        return True

    def get_metadata(self):
        """
        Get document metadata as dictionary
        :return: defaultdict of metadata, returning '' if
                 the field is not known
        """
        result = defaultdict(str)
        result.update(self.metadata)
        result['file_name'] = self.file_name
        return result
