import codecs
from functools import wraps
import os

import cjson


class DIRTFileException(Exception):
    pass


def unicode_error_handler(fn):
    """
    Capture and present unicode errors
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            val = fn(*args, **kwargs)
        except (cjson.DecodeError, UnicodeDecodeError) as e:
            template = u'Error {err} in {func_name} with args {args},{kwargs}'
            msg = template.format(err=str(e),
                                  func_name=str(fn),
                                  args=args,
                                  kwargs=kwargs)
            raise DIRTFileException(msg)
        return val
    return wrapped


@unicode_error_handler
def read_utf8(file_name):
    """
    Read a utf8 coded file
    :param file_name: name of file
    :return: unicode string of file
    """
    # fn = unicode(file_name).encode('ascii')
    fn = file_name
    with codecs.open(fn, encoding='utf8') as f:
        raw_passage = f.read()
    return raw_passage


@unicode_error_handler
def read_json_utf8(file_name):
    """
    Read a utf8 encoded json file
    :param file_name: name of file
    :return: dictionary that json file represents
    """
    raw = read_utf8(file_name)
    return cjson.decode(raw)


def write_json_utf8(file_name, serializable):
    """
    Convert a serializable object to json and write it to a file
    :param file_name: name of file to write to
    :param serializable: object to be serialized and written
    """
    json_rep = cjson.encode(serializable)
    unicode_json_rep = json_rep.decode('unicode_escape')
    write_utf8(file_name, unicode_json_rep)


def exists(file_name):
    """
    Does file exist
    :param file_name: full path to file
    :return: boolean
    """
    return os.path.exists(file_name)


def get_full_file_name(relative_file, magic_file):
    """
    Get fully quantified file name
    :param relative_file: file name relative to magic file
    :param magic_file: __file__ of calling module
    :return:
    """
    raw_loc = os.path.realpath(magic_file)
    my_dir = os.path.dirname(raw_loc)
    real_file_name = os.path.join(my_dir, relative_file)
    return real_file_name


def write_utf8(file_name, text):
    """
    Write a utf8 coded file
    :param file_name:  name of file
    :param text: file contents
    """
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    with codecs.open(file_name, 'w+', encoding='utf8') as f:
        f.write(text)


def get_file_name_only(full_path):
    """
    Get onlu the file name part of a full path
    :param full_path: full path
    :return: filename part of the input
    """
    file_name = os.path.basename(full_path)
    return file_name