import os

from models.document import Document
from preprocessing.tei.reader import TEIReader
import preprocessing.preprocessor as preprocessor
import utilities.decorators as decorators
import utilities.file_ops as file_ops
import utilities.path as path


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
def from_file(file_name, pre_dir=preprocessor.PREPROCESS_DIR):
    lowered_file_name = file_name.lower()
    if 'tei' in lowered_file_name:
        creator = from_tei
    elif 'json' in lowered_file_name:
        creator = from_json
    elif 'txt' in lowered_file_name:
        creator = from_txt
    else:
        template = 'Input file {file_name} is not a valid file type'
        msg = template.format(file_name=file_name)
        raise InvalidDocumentException(msg)
    return creator(file_name, pre_dir)


@unicode_error_handler
def from_txt(file_name, pre_dir):
    # body = file_ops.read_utf8(file_name)
    # TODO: handle pre names
    return Document(file_name=file_name,
                    raw_file_name=file_name)


@unicode_error_handler
def from_tei(file_name, pre_dir):
    reader = TEIReader(file_name)
    body, metadata = reader.read()
    name = path.get_name(file_name, extension=False)
    name_only = name + preprocessor.PREPROCESS_SUFFIX
    pre_name = os.path.join(pre_dir, name_only)
    file_ops.write_string(file_name=pre_name, to_write=body)
    # Write raw body
    return Document(file_name=file_name,
                    raw_file_name=pre_name,
                    pre_file_name=''
                    )


@unicode_error_handler
def from_json(file_name, pre_dir):
    data = file_ops.read_json_utf8(file_name)
    return Document(file_name=data['file_name'],
                    raw_file_name=data['file_name'],
                    metadata=data['metadata'],
                    pre_file_name=data['pre_file_name'])
