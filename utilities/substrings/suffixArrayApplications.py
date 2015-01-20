# -*- coding: utf-8 -*-
"""
Based on https://github.com/baiyubin/pysuffix
by Yubin Bai
"""
import tools_karkkainen_sanders as tks


def all_common_substrings(a, b, separator='$'):
    """
    all substrings in both a and b
    such that no substring is a substring of another substring
    """
    if separator in a or separator in b:
        raise Exception('Separator in input strings')
    ab = u''.join([a, separator, b])
    sa = tks.simple_kark_sort(ab)
    lcp = tks.LCP(ab, sa)
    sep = ab.index(separator)
    all_subs = set()

    for i, v in enumerate(lcp):
        if i >= sep and sa[i]+v > sep:
            passage = ab[sa[i]-1:sa[i] + v]
            to_remove = set()
            if passage not in all_subs:
                take = True
                for s in all_subs:
                    if passage in s:
                        take = False
                        break
                    elif s in passage:
                        to_remove.add(s)
                all_subs -= to_remove
                if take:
                    all_subs.add(passage)

    return all_subs


def search(text, to_find):
    """
    find first substring text
    """
    sa = tks.simple_kark_sort(to_find)
    m = len(text)
    n = len(to_find)
    left,  right = 0, n  # length of sa is n+1
    while left < right:
        mid = (left + right) >> 1
        comp = cmp(to_find[sa[mid]:sa[mid] + m], text)
        if comp >= 0:
            right = mid
        else:
            left = mid + 1
    if to_find[sa[left]: sa[left] + m] == text:
        return sa[left]
    else:
        return -1


def search2(text, to_find):
    """
    find the substring text, all occurrences
    """
    sa = tks.simple_kark_sort(to_find)
    m = len(text)
    n = len(to_find)
    left,  right = 0, n  # length of sa is n+1
    while left < right:
        mid = (left + right) >> 1
        comp = cmp(to_find[sa[mid]:sa[mid] + m], text)
        if comp >= 0:
            right = mid
        else:
            left = mid + 1
    start = left
    if to_find[sa[left]: sa[left] + m] != text:
        return []

    # upper bound
    left,  right = 0, n  # length of sa is n+1
    while left < right:
        mid = (left + right) >> 1
        comp = cmp(to_find[sa[mid]:sa[mid] + m], text)
        if comp > 0:
            right = mid
        else:
            left = mid + 1
    end = left
    result = [sa[i] for i in range(start, end)]
    result.sort()
    return result
