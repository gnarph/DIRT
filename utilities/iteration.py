def niter(s, n):
    """
    Iterate over s, n elements at a time
    :param s: object to iterate over (str)
    :param n: number of elements to return at once
    :return: generator
    """
    for i in xrange(len(s) - n - 1):
        yield s[i:i+n]