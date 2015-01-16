from collections import namedtuple
from cpython cimport array
from array import array
import numpy as np


MatchBlock = namedtuple('MatchBlock', ['a', 'b', 'size'])


cpdef object lcs(basestring a, basestring b):
    cdef int m = len(a)
    cdef int n = len(b)
    cdef int c, i, j
    narr = np.zeros((m, n), dtype=np.int32)
    cdef int [:, :] counter = narr

    results = set()
    for i in xrange(m-1):
        for j in xrange(n-1):
            if a[i] == b[j]:
                c = counter[i, j] + 1
                counter[i+1, j+1] = c
                new_match = a[i-c+1:i+1]
                results.add(new_match)

    return results


def matched_passages(basestring a, basestring b):
    cdef int a_space_start
    cdef int b_space_start
    cdef basestring a_added_spc
    cdef basestring b_added_spc

    a_spaces = space_locations(a)
    b_spaces = space_locations(b)

    a_strip = a.replace(' ', '')
    b_strip = b.replace(' ', '')

    substrings = lcs(a_strip, b_strip)

    for substring in substrings:
        a_space_start = a_strip.index(substring)
        b_space_start = b_strip.index(substring)

        a_added_spc = add_spaces(space_locations=a_spaces,
                                 offset=a_space_start,
                                 target=substring)
        b_added_spc = add_spaces(space_locations=b_spaces,
                                 offset=b_space_start,
                                 target=substring)
        yield a_added_spc, b_added_spc


def add_spaces(int[:] space_locations, int offset, basestring target):
    cdef int end = offset + len(target)
    cdef last = 0
    insert_points = (i - offset for i in space_locations if offset <= i <= end)

    chunks = []
    for point in insert_points:
        chunks += [target[last:point]]
        last = point
    chunks += [target[last:]]
    return u' '.join(chunks)


cpdef int[:] space_locations(basestring s):
    cdef array.array spaces = array('i', [])
    cdef array.array j
    cdef int new_index
    cdef int i
    cdef basestring c

    for i, c in enumerate(s):
        if c == ' ':
            new_index = i - len(spaces)
            j = array('i', [new_index])
            spaces.extend(j)
    return spaces
