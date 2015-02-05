from array import array


def respace(body, stripped_body, passages):
    spaces = space_locations(body)
    new_passages = []
    for p in passages:
        offset = stripped_body.index(p)
        np = add_spaces(spaces, offset, p)
        np = np.strip(u' \t\r\n')
        new_passages.append(np)
    return new_passages


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


def add_spaces(space_locs, offset, target):
    """
    Put spaces back into stripped string
    :param space_locs: where to insert spaces into body to restore it
    :param offset: location of target within it's body
    :param target: passage from a body
    :return:
    """
    end = offset + len(target)
    last = 0
    insert_points = (i - offset for i in space_locs if offset <= i <= end)

    chunks = []
    for point in insert_points:
        if last != point:
            chunks += [target[last:point]]
        last = point
    if target[last:]:
        chunks += [target[last:]]
    return u' '.join(chunks)
