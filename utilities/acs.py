from collections import namedtuple
from array import array
import numpy as np


MatchBlock = namedtuple('MatchBlock', ['a', 'b', 'size'])


def lcs(a, b):
    """
    Do a thing
    :param a: String to compare
    :param b: String to compare
    :return: set of common substrings
    """
    # Need to add jump gap here
    m = len(a)
    n = len(b)
    narr = np.zeros((m+1, n+1), dtype=np.int32)
    counter = narr

    results = set()
    # Basically longest common substring algorithm
    # Except that we look for all common substrings
    # rather than just the longest one
    for i in xrange(m):
        for j in xrange(n):
            if a[i] == b[j]:
                c = counter[i, j] + 1
                counter[i+1, j+1] = c
                new_match = a[i-c+1:i+1]
                if new_match:
                    results.add(new_match)

    return counter


def common_passages(a, b, jump_gap, match_length):
    substring_array = lcs(a, b)
    m = len(a)
    n = len(b)

    # If substrings are close enough together, stick them together
    for i in xrange(m):
        for j in xrange(n):
            if substring_array[i, j] > 0:
                # We have a substring, so attempt to extend
                extend_match(substring_array, m, n, i, j, jump_gap)

    # Get the substrings out of the array
    passages = set()
    for i in xrange(m):
        for j in xrange(n):
            if substring_array[i, j] == 1:
                # start new passage
                x = i + 1
                y = j + 1
                while x < m+1 and y < n+1 and substring_array[x, y] != 0:
                    x += 1
                    y += 1


def extend_match(substring_array, m, n, i_start,
                    j_start, jump_gap):
    i = i_start + 1
    j = j_start + 1
    jump = 1

    if i < m+1 and j < n+1 and substring_array[i, j] > 0:
        # Substring continues anyway or there is no more string
        # to compare
        return

    # If the substring would otherwise terminate attempt
    # to jump the gap
    while i < m+1 and j < n+1 and jump < jump_gap:
        jump += 1
        i += 1
        j += 1

        if substring_array[i, j] > 0:
            # Extend the substring!
            prev_len = substring_array[i_start, j_start]
            for x in xrange(i_start+1, i):
                for y in xrange(j_start+1, j):
                    substring_array[x, y] = prev_len + 1
                    prev_len = substring_array[x, y]
            return


def matched_passages(a, b):
    skip = False

    a_spaces = space_locations(a)
    b_spaces = space_locations(b)

    a_strip = a.replace(' ', '')
    b_strip = b.replace(' ', '')

    substrings = lcs(a_strip, b_strip)

    # should remove items from substrings
    # that are substrings of other items
    ordered_subs = sorted(list(substrings), key=len, reverse=True)
    take = []
    for s in ordered_subs:
        for t in take:
            skip = s in t
            if skip:
                break
        if skip:
            continue
        take.append(s)
    substrings = take
    print take

    for substring in substrings:
        # Find where in the stripped body a passage appears
        a_space_start = a_strip.index(substring)
        b_space_start = b_strip.index(substring)

        # Put the spaces back into passages so we can find
        # them within the original text
        a_added_spc = add_spaces(space_locations=a_spaces,
                                 offset=a_space_start,
                                 target=substring)
        b_added_spc = add_spaces(space_locations=b_spaces,
                                 offset=b_space_start,
                                 target=substring)
        yield a_added_spc, b_added_spc


def add_spaces(space_locations, offset, target):
    """
    Put spaces back into stripped string
    :param space_locations: where to insert spaces into body to restore it
    :param offset: location of target within it's body
    :param target: passage from a body
    :return:
    """
    end = offset + len(target)
    last = 0
    insert_points = (i - offset for i in space_locations if offset <= i <= end)

    chunks = []
    for point in insert_points:
        chunks += [target[last:point]]
        last = point
    chunks += [target[last:]]
    return u' '.join(chunks)


def space_locations(s):
    """
    Get the locations to insert spaces to restore original string
    after spaces are stripped out
    :param s: string with spaces which will later be stripped
    :return: int array of indices to insert spaces to restore original
             string
    """
    spaces = array('i', [])

    for i, c in enumerate(s):
        if c == ' ':
            new_index = i - len(spaces)
            j = array('i', [new_index])
            spaces.extend(j)
    return spaces
