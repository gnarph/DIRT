"""
Base comparator
"""


class BaseComparator(object):
    """
    Base comparator class
    """
    def __init__(self, a, b, match_length=10, gap_length=3):
        self.a = a
        self.b = b
        self.match_length = match_length
        self.gap_length = gap_length
