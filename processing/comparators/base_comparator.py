"""
Base comparator
"""


class BaseComparator(object):
    """
    Base comparator class
    """
    def __init__(self, file_name_a, file_name_b, match_length=10, gap_length=3):
        self.file_name_a = file_name_a
        self.file_name_b = file_name_b
        self.match_length = match_length
        self.gap_length = gap_length
