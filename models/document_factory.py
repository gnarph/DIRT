from models.document import Document
from preprocessing.tei.reader import TEIReader
import utilities.decorators as decorators
import utilities.file_reading as file_reading


class InvalidDocumentException(BaseException):
    pass


def unicode_error_handler(fn):
    def wrapped(*args, **kwargs):
        try:
            val = fn(*args, **kwargs)
        except UnicodeDecodeError as e:
            tmpl = u'Error {err} in {func_name} with args {args},{kwargs}'
            msg = tmpl.format(err=str(e),
                              func_name=str(fn),
                              args=args,
                              kwargs=kwargs)
            raise InvalidDocumentException(msg)
        return val
    return wrapped


# Possible problem with significant memory use of documents
@decorators.memoize_single_arg
def from_file(file_name):
    lowered_file_name = file_name.lower()
    if 'tei' in lowered_file_name:
        creator = from_tei
    elif 'json' in lowered_file_name:
        creator = from_json
    elif 'txt' in lowered_file_name:
        creator = from_txt
    else:
        tmpl = 'Input file {file_name} is not a valid file type'
        msg = tmpl.format(file_name=file_name)
        raise InvalidDocumentException(msg)
    return creator(file_name)


@unicode_error_handler
def from_txt(file_name):
    body = file_reading.read_utf8(file_name)
    return Document(file_name, body)


@unicode_error_handler
def from_tei(file_name):
    reader = TEIReader(file_name)
    return reader.read()


@unicode_error_handler
def from_json(file_name):
    data = file_reading.read_json_utf8(file_name)
    return Document(file_name=data['file_name'],
                    body=data['body'],
                    metadata=data['metadata'])
