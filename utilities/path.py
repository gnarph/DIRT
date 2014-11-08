import os


def iter_files_in(directory):
    # TODO: Consider os.walk for finding recursively
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
    return name[0] == '.'


def get_name(filename, extension=True):
    fn = filename if extension else os.path.splitext(filename)[0]
    return os.path.split(fn)[1]
