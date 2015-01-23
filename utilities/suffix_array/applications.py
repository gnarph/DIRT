# -*- coding: utf-8 -*-
"""
Based on https://github.com/baiyubin/pysuffix
by Yubin Bai
"""
from collections import namedtuple
import itertools
import re

import utilities.suffix_array.tools_karkkainen_sanders as tks


class InvalidCharacterException(Exception):
    pass


MB = namedtuple('MatchBlock',
                field_names=['a', 'b', 'l', 'passage'])


class MatchBlock(MB):

    def __hash__(self):
        return self[0] * self[1] * self[2]

    def __eq__(self, other):
        if self[0] != other[0]:
            return False
        elif self[1] != other[1]:
            return False
        elif self[2] != other[2]:
            return False
        return True


def all_common_substrings(a, b, separator='$'):
    """
    Find all substrings in both a and b
    :param a: first string
    :param b: second string
    :param separator: character to be used to separate a and b
                      when creating a suffix array. Cannot
                      appear in a or b
    :return: set of strings appearing in both a and b
    """
    if separator in a or separator in b:
        raise InvalidCharacterException('Separator in input strings')
    ab = u''.join([a, separator, b])
    sa = tks.simple_kark_sort(ab)
    lcp = tks.LCP(ab, sa)
    all_subs = set()

    for i, v in enumerate(lcp):
        start = sa[i]
        end = start + v
        p = ab[start:end]

        # if end - start < min_match:
        #     continue
        if not p or p not in a or p not in b:
            continue

        # TODO: p could occur twice in a and/or b
        p_esc = re.escape(p)
        a_starts = (m.start() for m in re.finditer(p_esc, a))
        b_starts = (m.start() for m in re.finditer(p_esc, b))
        for a_start, b_start in itertools.product(a_starts, b_starts):
            tup = MatchBlock(a_start, b_start, v, p)
            if tup not in all_subs:
                to_remove = set()
                take = True
                for s in all_subs:
                    # also need to check indices of appearance
                    # in other string
                    sa_end = s.a + s.l
                    sb_end = s.b + s.l
                    a_end = a_start + v
                    b_end = b_start + v
                    contained_a = a_start >= s.a and a_end <= sa_end
                    contained_b = b_start >= s.b and b_end <= sb_end
                    if contained_a and contained_b:
                        # If we p is a substring of s
                        # we don't want to take it so we can leave
                        take = False
                        break
                    else:
                        contains_a = s.a >= a_start and sa_end <= a_end
                        contains_b = s.b >= b_start and sb_end <= b_end
                        if contains_a and contains_b:
                            # We want to remove s if it is superseded
                            # by p
                            to_remove.add(s)
                all_subs -= to_remove
                if take:
                    all_subs.add(tup)

    # Hack to get things working right now
    return [x.passage for x in all_subs]
