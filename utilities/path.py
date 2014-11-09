import os
import shutil


def iter_files_in(directory):
    # TODO: Consider os.walk for finding recursively
    # however, then the processing naming would probably need
    # to be adjusted
    for item_name in os.listdir(directory):
        if should_use_file(item_name):
            yield os.path.join(directory, item_name)


def should_use_file(name):
    if os.path.isdir(name):
        return False
    if is_hidden_file(name):
        return False
    return True


def is_hidden_file(name):
    """
    Is a file hidden?
    :param name: name of file
    :return: True or False
    """
    return name[0] == '.'


def get_name(filename, extension=True):
    """
    Get name of a file without the path portion
    :param filename: path of file
    :param extension: include the extension?
    :return: name of file without path
    """
    fn = filename if extension else os.path.splitext(filename)[0]
    return os.path.split(fn)[1]


def delete_folder(name):
    """
    Deletes folder, if folder does not exist, fails silently
    :param name: name/path of folder to delete
    """
    try:
        shutil.rmtree(name)
    except OSError:
        pass


def create_folder(name):
    """
    Creates a folder
    :param name: folder name/path
    """
    os.makedirs(name)


def reset_folder(name):
    """
    Cleanout a folder
    :param name: folder to clean out
    :return:
    """
    delete_folder(name)
    create_folder(name)
