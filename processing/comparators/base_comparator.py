"""
Base comparator
"""


class BaseComparator(object):
    """
    Base comparator class
    :param a: first document to compare
    :param b: second document to compare
    :param match_length: minimum length for a match
    :param gap_length: max length of gap within a match
    """
    def __init__(self, a, b, name_a, name_b, match_length=10, gap_length=3):
        self.a = a
        self.b = b
        self.a_strip = a.replace(' ', '')
        self.b_strip = b.replace(' ', '')
        self.name_a = name_a
        self.name_b = name_b
        self.match_length = match_length
        self.gap_length = gap_length
