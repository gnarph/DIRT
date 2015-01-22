# -*- coding: utf-8 -*-
"""
Based on https://github.com/baiyubin/pysuffix
by Yubin Bai
"""
import utilities.suffix_array.tools_karkkainen_sanders as tks


class InvalidCharacterException(Exception):
    pass


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
        if not p:
            continue

        # Checking passage in a|b in case the passage occurs twice in
        # a or twice in b
        tup = (start, end, p)
        if tup not in all_subs:
            to_remove = set()
            take = True
            for s in all_subs:
                # also need to check indices of appearance
                # in other string
                if start >= s[0] and end <= s[1]:
                    # If we p is a substring of s
                    # we don't want to take it so we can leave
                    take = False
                    break
                elif s[0] >= start and s[1] <= end:
                    # We want to remove s if it is superseded
                    # by p
                    to_remove.add(s)
            all_subs -= to_remove
            if take:
                all_subs.add(tup)

    # Hack to get things working right now
    return [x[2] for x in all_subs]
