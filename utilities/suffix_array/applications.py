# -*- coding: utf-8 -*-
"""
Based on https://github.com/baiyubin/pysuffix
by Yubin Bai
"""
from collections import namedtuple

import utilities.suffix_array.tools_karkkainen_sanders as tks


class InvalidCharacterException(Exception):
    pass


MatchBlock = namedtuple('MatchBlock',
                        field_names=['a', 'b', 'l', 'passage'])


def all_common_substrings(a, b, separator='$'):
    """
    Find all substrings in both a and b
    such that no substring is a substring of another substring
    :param a: first string
    :param b: second string
    :param separator: character to be used to separate a and b
                      when creating a suffix array. Cannot
                      appear in a or b
    :return: set of strings appearing in both a and b,
             which is not a substring of another string in the set
    """
    # TODO: test if we actually want the substring constraint in
    #       the return value
    if separator in a or separator in b:
        raise InvalidCharacterException('Separator in input strings')
    ab = u''.join([a, separator, b])
    sa = tks.simple_kark_sort(ab)
    lcp = tks.LCP(ab, sa)
    all_subs = set()

    for i, v in enumerate(lcp):
        # Only want something that is present in
        # a AND b, not a AND a or b AND b
        start = sa[i]
        end = start + v
        p = ab[start:end]

        # Empty strings are not matches
        if not p or p not in a or p not in b:
            continue

        # TODO: p could occur twice in a and/or b
        a_start = a.index(p)
        b_start = b.index(p)
        tup = MatchBlock(a_start, b_start, v, p)
        if tup not in all_subs:
            to_remove = set()
            take = True
            for s in all_subs:
                # also need to check indices of appearance
                # in other string
                contained_a = a_start >= s.a and v <= s.l
                contained_b = b_start >= s.b and v <= s.l
                if contained_a and contained_b:
                    # If we p is a substring of s
                    # we don't want to take it so we can leave
                    take = False
                    break
                else:
                    contains_a = s.a >= a_start and s.l <= v
                    contains_b = s.b >= b_start and s.l <= v
                    if contains_a and contains_b:
                        # We want to remove s if it is superseded
                        # by p
                        to_remove.add(s)
            all_subs -= to_remove
            if take:
                all_subs.add(tup)

    # Hack to get things working right now
    return [x.passage for x in all_subs]
