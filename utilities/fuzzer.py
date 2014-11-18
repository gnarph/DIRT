"""
Fuzzy finding using fuzzywuzzy/Levenshtein distance
"""

from fuzzywuzzy import process as fuzzy_process
from fuzzywuzzy import fuzz

from utilities.iteration import niter

SCORE_CUTOFF = 60


class FuzzerFailure(BaseException):
    pass


def find_in_body(body, passage, match_limit=5, score_cutoff=SCORE_CUTOFF):
    len_passage = len(passage)
    len_body = len(body)
    if len_passage >= len_body:
        return 0, len_body
    # this isn't working with zhi
    # maybe try looking for parts of the passage
    body_gen = niter(body, len_passage*2)
    search_dict = dict(enumerate(body_gen))
    # list of tuples (body str, score/100, index in body)
    matches = fuzzy_process.extractBests(query=passage,
                                         choices=search_dict,
                                         scorer=fuzz.UQRatio,
                                         limit=match_limit)
    indices = [tup[2] for tup in matches]
    try:
        min_index = min(indices)
        max_index = max(indices) + len_passage
    except ValueError:
        template = u'Unable to find {} in {}'
        message = template.format(passage, body)
        print message
        raise FuzzerFailure(message)
    return min_index, max_index


def is_fuzzy_match(a, b, score_cutoff=SCORE_CUTOFF):
    return fuzz.ratio(a, b) > score_cutoff