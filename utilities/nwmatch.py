"""
Do matching with Needleman-Wunsh alignment (global alginment algorithm)
"""

import re

import nwalign

RE_NOT_DASH = r'([^-])'


def find_in_body(body, passage):
    """
    Find the start and end indices of a passage in a body
    Exact match needs to be there though or it will not work
    """
    s_body = body.encode('utf8')
    s_passage = passage.encode('utf8')
    aligned_tuple = nwalign.global_align(s_body, s_passage)
    aligned_passage = aligned_tuple[1]
    start_match = re.search(RE_NOT_DASH, aligned_passage)
    # Starting index of passage in body, probably
    start = start_match.start()
    reverse_aligned_passage = ''.join(reversed(aligned_passage))
    end_match = re.search(RE_NOT_DASH, reverse_aligned_passage)
    # Ending index of passage in body, probably
    end = len(s_body) - end_match.end()
    print s_body[start:end]
    return start, end
