import os

from processing import processor
import utilities.file_ops as file_reading
from models.match_set import MatchSet


class NoMatchSetFoundException(Exception):
    pass


def from_json(file_name):
    """
    Create a MatchSet from a json file
    :param file_name: name of json file
    :return: MatchSet
    """
    data = file_reading.read_json_utf8(file_name)
    return MatchSet.from_dict(data)


def _get_report_name(directory, name_a, name_b):
    """
    Get the name of a report comparing two documents
    :param directory: directory containing MatchSet json files
    :param name_a: name of first document
    :param name_b: name of second document
    :return: path to MatchSet json file comparing documents
    """
    name = processor.REPORT_NAME.format(name_a, name_b)
    full = os.path.join(directory, name)
    return full


def find_in_dir(name_a, name_b, directory):
    """
    Get a match set from a directory containing output files
    :param name_a: doc name a
    :param name_b: doc name b
    :param directory: directory of output files
    :return: MatchSet
    """
    full = _get_report_name(directory, name_a, name_b)
    try:
        ms = from_json(full)
    except IOError:
        full = _get_report_name(directory, name_b, name_a)
        try:
            ms = from_json(full)
        except IOError:
            template = "Could not find match for {} and {} in {}"
            message = template.format(name_a, name_b, directory)
            raise NoMatchSetFoundException(message)
        else:
            ms.swap_alpha_beta()
    return ms
