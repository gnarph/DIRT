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
    all substrings in both a and b
    such that no substring is a substring of another substring
    """
    if separator in a or separator in b:
        raise InvalidCharacterException('Separator in input strings')
    ab = u''.join([a, separator, b])
    sa = tks.simple_kark_sort(ab)
    lcp = tks.LCP(ab, sa)
    sep = ab.index(separator)
    all_subs = set()

    for i, v in enumerate(lcp):
        # Only want something that is present in
        # a AND b, not a AND a or b AND b
        start = sa[i]
        end = start + v
        p = ab[start:end]
        # Checking passage in a|b in case the passage occurs twice in
        # a or twice in b
        if (start > sep and p in a) or (end <= sep and p in b):
            if p not in all_subs:
                to_remove = set()
                take = True
                for s in all_subs:
                    # Current strategy aims to keep memory use
                    # lower, could go faster if this filtering
                    # was done after the fact
                    if p in s:
                        # If we p is a substring of s
                        # we don't want to take it so we can leave
                        take = False
                        break
                    elif s in p:
                        # We want to remove s if it is superceded
                        # by p
                        to_remove.add(s)
                all_subs -= to_remove
                if take:
                    all_subs.add(p)

    return all_subs
