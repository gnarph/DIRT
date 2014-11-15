from utilities import file_ops


class InvalidDocumentException(BaseException):
    pass


def error_handler(fn):
    def wrapped(*args, **kwargs):
        try:
            val = fn(*args, **kwargs)
        except (UnicodeDecodeError, KeyError) as e:
            tmpl = u'Error {err} in {func_name} with args {args},{kwargs}'
            msg = tmpl.format(err=str(e),
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
            raise Exception(template)
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
        return file_ops.read_utf8(self.raw_file_name)

    @property
    def pre_body(self):
        return file_ops.read_utf8(self.pre_file_name)

    def clone(self):
        return Document(file_name=self.file_name,
                        metadata=self.metadata,
                        pre_file_name=self.pre_file_name,
                        raw_file_name=self.raw_file_name)

    def to_dict(self):
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
