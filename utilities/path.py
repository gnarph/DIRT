import os
import shutil


def iter_files_in(directory):
    """
    Iterate over all filenames in a directory
    Does not descend into sub-directories
    :param directory: directory to look for
    :return: generator
    """
    for item_name in os.listdir(directory):

        full_name = os.path.join(directory, item_name)
        print full_name, directory
        if should_use_file(full_name):
            yield full_name


def should_use_file(name):
    """
    Should DIRT use the file?
    :param name: name of file
    :return: boolean
    """
    if is_hidden_file(name):
        return False
    return os.path.isfile(name)


def is_hidden_file(full_name):
    """
    Is a file hidden?
    :param full_name: name of file
    :return: True or False
    """
    name = get_name(full_name)
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
