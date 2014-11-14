import utilities.file_ops as file_reading
from models.match_set import MatchSet


def from_json(file_name):
    data = file_reading.read_json_utf8(file_name)
    return MatchSet.from_dict(data)