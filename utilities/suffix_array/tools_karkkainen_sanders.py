# -*- coding: utf-8 -*-
"""
Originally from https://code.google.com/p/pysuffix/
Used from  https://github.com/baiyubin/pysuffix
"""
from array import array


def radix_pass(a, b, r, n, k):
    """
    :param a: word to sort
    :param b: sorted words
    :param r: initial string
    :param n: input size
    :param k: alphabet size
    """
    c = array("i", [0] * (k + 1))
    for i in xrange(n):
        c[r[a[i]]] += 1
    somme = 0
    for i in xrange(k + 1):
        freq, c[i] = c[i], somme
        somme += freq
    for i in xrange(n):
        b[c[r[a[i]]]] = a[i]
        c[r[a[i]]] += 1


def simple_kark_sort(s):
    alphabet = [None] + sorted(set(s))
    k = len(alphabet)
    alphabet_indices = {c: i for i, c in enumerate(alphabet)}
    n = len(s)
    sa = array('i', [0] * (n + 3))
    s = array('i', [alphabet_indices[c] for c in s] + [0] * 3)
    kark_sort(s, sa, n, k)
    return sa


def kark_sort(to_sort, result, n, alphabet_size):
    """s  : word to sort
       SA : result
       n  : len of s
       K  : alphabet size"""
    n0 = (n + 2) / 3
    n1 = (n + 1) / 3
    n2 = n / 3
    n02 = n0 + n2
    sa_12 = array('i', [0] * (n02 + 3))
    sa_0 = array('i', [0] * n0)

    s12 = [i for i in xrange(n + (n0 - n1)) if i % 3]
    s12.extend([0] * 3)
    s12 = array('i', s12)

    radix_pass(s12, sa_12, to_sort[2:], n02, alphabet_size)
    radix_pass(sa_12, s12, to_sort[1:], n02, alphabet_size)
    radix_pass(s12, sa_12, to_sort, n02, alphabet_size)

    name = 0
    c0, c1, c2 = -1, -1, -1
    for i in xrange(n02):
        if to_sort[sa_12[i]] != c0 or to_sort[sa_12[i] + 1] != c1 or to_sort[sa_12[i] + 2] != c2:
            name += 1
            c0 = to_sort[sa_12[i]]
            c1 = to_sort[sa_12[i] + 1]
            c2 = to_sort[sa_12[i] + 2]
        if sa_12[i] % 3 == 1:
            s12[sa_12[i] / 3] = name
        else:
            s12[sa_12[i] / 3 + n0] = name
    if name < n02:
        kark_sort(s12, sa_12, n02, name + 1)
        for i in xrange(n02):
            s12[sa_12[i]] = i + 1
    else:
        for i in xrange(n02):
            sa_12[s12[i] - 1] = i
    s0 = array('i', [sa_12[i] * 3 for i in xrange(n02) if sa_12[i] < n0])
    radix_pass(s0, sa_0, to_sort, n0, alphabet_size)
    p = j = alphabet_size = 0
    t = n0 - n1
    while alphabet_size < n:
        if sa_12[t] < n0:
            i = sa_12[t] * 3 + 1
        else:
            i = (sa_12[t] - n0) * 3 + 2
        j = sa_0[p] if p < n0 else 0
        if sa_12[t] < n0:
            if to_sort[i] == to_sort[j]:
                test = s12[sa_12[t] + n0] <= s12[j / 3]
            else:
                test = to_sort[i] < to_sort[j]
        elif to_sort[i] == to_sort[j]:
            if to_sort[i + 1] == to_sort[j + 1]:
                test = s12[sa_12[t] - n0 + 1] <= s12[j / 3 + n0]
            else:
                test = to_sort[i + 1] < to_sort[j + 1]
        else:
            test = to_sort[i] < to_sort[j]
        if test:
            result[alphabet_size] = i
            t += 1
            if t == n02:
                alphabet_size += 1
                while p < n0:
                    result[alphabet_size] = sa_0[p]
                    p += 1
                    alphabet_size += 1
        else:
            result[alphabet_size] = j
            p += 1
            if p == n0:
                alphabet_size += 1
                while t < n02:
                    if sa_12[t] < n0:
                        result[alphabet_size] = (sa_12[t] * 3) + 1
                    else:
                        result[alphabet_size] = ((sa_12[t] - n0) * 3) + 2
                    t += 1
                    alphabet_size += 1
        alphabet_size += 1


def longest_common_prefixes(s, suffix_array):
    """
    return LCP array that LCP[i] is the longest common prefix
    between s[SA[i]] and s[SA[i+1]]
    """
    n = len(s)
    rank = array('i', [0] * n)
    lcp = array('i', [0] * n)
    for i in xrange(n):
        rank[suffix_array[i]] = i
    l = 0
    for j in xrange(n):
        l = max(0, l - 1)
        i = rank[j]
        j2 = suffix_array[i - 1]
        if i:
            while l + j < n and l + j2 < n and s[j + l] == s[j2 + l]:
                l += 1
            lcp[i - 1] = l
        else:
            l = 0
    return lcp
