"""
Fuzzy finding using fuzzywuzzy/Levenshtein distance
"""

from fuzzywuzzy import process as fuzzy_process
from fuzzywuzzy import fuzz

from utilities.iteration import niter


class FuzzerFailure(BaseException):
    pass


def find_in_body(body, passage, match_limit=5):
    len_passage = len(passage)
    len_body = len(body)
    if len_passage >= len_body:
        return 0, len_body
    # this isn't working with zhi
    # maybe try looking for parts of the passage
    body_gen = niter(body, len_passage)
    search_dict = dict(enumerate(body_gen))
    # list of tuples (body str, score/100, index in body)
    matches = fuzzy_process.extractBests(query=passage,
                                         choices=search_dict,
                                         scorer=fuzz.UQRatio,
                                         limit=match_limit)
    indices = [tup[2] for tup in matches]
    try:
        # TODO: this will mess up if there are good matches
        # in two areas of the document
        min_index = min(indices)
        max_index = max(indices) + len_passage
    except ValueError:
        template = u'Unable to find {} in {}'
        message = template.format(passage, body)
        print message
        raise FuzzerFailure(message)
    return min_index, max_index


def is_fuzzy_match(a, b, score_cutoff=90):
    return fuzz.ratio(a, b) > score_cutoff