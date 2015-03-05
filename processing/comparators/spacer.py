from array import array


def get_space_locations(s):
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
            # index of i after the space is removed
            new_index = i - len(spaces)
            j = array('i', [new_index])
            spaces.extend(j)
    return spaces


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
    insert_points = (i - offset for i in space_locations
                     if offset <= i <= end)

    started = False
    chunks = []
    for point in insert_points:
        # Avoid spaces at the start
        if started or last != point:
            started = True
            # Add string between target and point
            chunks += [target[last:point]]
        last = point
    # Avoid a space at the end
    if target[last:]:
        chunks += [target[last:]]
    return u' '.join(chunks)
