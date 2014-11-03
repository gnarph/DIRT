"""
Fuzzy finding using fuzzywuzzy/Levenshtein distance
"""

from fuzzywuzzy import process as fuzzy_process
from fuzzywuzzy import fuzz

from utilities.iteration import niter

SCORE_CUTOFF = 90


def find_in_body(body, passage, match_limit=5, score_cutoff=SCORE_CUTOFF):
    len_passage = len(passage)
    body_gen = niter(body, len_passage)
    search_dict = dict(enumerate(body_gen))
    # list of tuples (body str, score/100, index in body)
    matches = fuzzy_process.extractBests(query=passage,
                                         choices=search_dict,
                                         score_cutoff=score_cutoff,
                                         limit=match_limit)
    indices = [tup[2] for tup in matches]
    min_index = min(indices)
    max_index = max(indices) + len_passage
    return min_index, max_index


def is_fuzzy_match(a, b, score_cutoff=SCORE_CUTOFF):
    return fuzz.ratio(a, b) > score_cutoff