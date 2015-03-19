# -*- coding: utf-8 -*-
"""
Based on https://github.com/baiyubin/pysuffix
by Yubin Bai
"""
from collections import namedtuple
import itertools
import re

try:
    import pyximport
    pyximport.install()
    import utilities.suffix_array.tools_karkkainen_sandersx as tks
except ImportError:
    import utilities.suffix_array.tools_karkkainen_sanders as tks


class InvalidCharacterException(Exception):
    pass


MB = namedtuple('MatchBlock',
                field_names=['a', 'b', 'l', 'passage'])


class MatchBlock(MB):
    """
    NamedTuple subclass for representing match blocks
    """

    def __hash__(self):
        return self[0] * self[1] * self[2]

    def __eq__(self, other):
        """
        Equals method that avoids comparing the string potion
        of matches
        """
        if self[0] != other[0]:
            return False
        elif self[1] != other[1]:
            return False
        elif self[2] != other[2]:
            return False
        return True


# This is very slow, and as such is inaccessible
# should add option for using it or something similar later
def acs_all(a, b, separator='$'):
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
    lcp = tks.longest_common_prefixes(ab, sa)
    all_subs = set()

    for i, v in enumerate(lcp):
        start = sa[i]
        end = start + v
        p = ab[start:end]

        # Sanity check
        # Also p can't be an empty string
        if not p or p not in a or p not in b:
            continue

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


def acs_no_substrings(a, b, separator='$', cython=True):
    """
    all substrings in both a and b
    such that no substring is a substring of another substring
    """
    if cython:
        tools_ks = tks
    if not cython:
        import utilities.suffix_array.tools_karkkainen_sanders as tools_ks

    if separator in a or separator in b:
        raise InvalidCharacterException('Separator in input strings')

    # Need separator character to work with suffix array
    # Separator character must not occur in either a or b
    # Else a substring could cross the boundry between a and b
    ab = u''.join([a, separator, b])

    # Suffix array
    sa = tools_ks.simple_kark_sort(ab)

    # Longest common prefix array
    lcp = tools_ks.longest_common_prefixes(ab, sa)
    sep = ab.index(separator)
    all_subs = set()

    for i, v in enumerate(lcp):
        # Only want something that is present in
        # a AND b, not a AND a or b AND b
        passage = ab[sa[i]:sa[i] + v]
        # Checking passage in a|b in case the passage occurs twice in
        # a or twice in b
        if (sa[i] > sep and passage in a) or (sa[i]+v <= sep and passage in b):
            if passage not in all_subs:
                to_remove = set()
                take = True
                for s in all_subs:
                    if passage in s:
                        # If we p is a substring of s
                        # we don't want to take it so we can leave
                        take = False
                        break
                    elif s in passage:
                        # We want to remove s if it is a
                        # substring of by p
                        to_remove.add(s)
                all_subs -= to_remove
                if take:
                    all_subs.add(passage)

    return all_subs
