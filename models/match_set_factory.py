import os

from processing import processor
import utilities.file_ops as file_reading
from models.match_set import MatchSet


def from_json(file_name):
    data = file_reading.read_json_utf8(file_name)
    return MatchSet.from_dict(data)


def find_in_dir(name_a, name_b, directory):
    template = processor.REPORT_NAME
    name = template.format(name_a, name_b)
    full = os.path.join(directory, name)
    try:
        ms = from_json(full)
    except IOError:
        name = template.format(name_b, name_a)
        full = os.path.join(directory, name)
        ms = from_json(full)
    return ms
