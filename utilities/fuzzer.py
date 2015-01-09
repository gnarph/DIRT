"""
Fuzzy finding using fuzzywuzzy/Levenshtein distance
"""

from fuzzywuzzy import process as fuzzy_process
from fuzzywuzzy import fuzz

from utilities.iteration import niter


def is_fuzzy_match(a, b, score_cutoff=90):
    """
    Checks if two (unicode) strings are a fuzzy match
    :param a: unicode string
    :param b: unicode string
    :param score_cutoff: integer percentage that consitutes a match
    :return: true or false
    """
    return fuzz.ratio(a, b) > score_cutoff