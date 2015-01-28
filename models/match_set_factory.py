import os

from processing import processor
import utilities.file_ops as file_reading
from models.match_set import MatchSet


def from_json(file_name):
    data = file_reading.read_json_utf8(file_name)
    return MatchSet.from_dict(data)


def _get_report_name(directory, name_a, name_b):
    name = processor.REPORT_NAME.format(name_a, name_b)
    full = os.path.join(directory, name)
    return full


def find_in_dir(name_a, name_b, directory):
    # TODO: consider ensuring that MatchSet.alpha_doc
    #       refers to name_a
    full = _get_report_name(directory, name_a, name_b)
    try:
        ms = from_json(full)
    except IOError:
        full = _get_report_name(directory, name_b, name_a)
        ms = from_json(full)
    return ms
