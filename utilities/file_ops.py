import codecs
import os

import cjson


def read_utf8(file_name):
    """
    Read a utf8 coded file
    :param file_name: name of file
    :return: unicode string of file
    """
    with codecs.open(file_name, encoding='utf-8') as f:
        raw_passage = f.read()
    return raw_passage


def read_json_utf8(file_name):
    """
    Read a utf8 encoded json file
    :param file_name: name of file
    :return: dictionary that json file represents
    """
    raw = read_utf8(file_name)
    return cjson.decode(raw)


def write_json_utf8(file_name, serializable):
    json_rep = cjson.encode(serializable)
    unicode_json_rep = json_rep.decode('unicode_escape')
    write_utf8(file_name, unicode_json_rep)


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


def write_utf8(full_name, to_write):
    """
    Write a utf8 coded file
    :param file_name:  name of file
    :param text: file contents
    """
    if not os.path.exists(os.path.dirname(full_name)):
        os.makedirs(os.path.dirname(full_name))
    with codecs.open(full_name, 'w+', encoding='utf8') as f:
        f.write(to_write)
