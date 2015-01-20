from collections import defaultdict
import pysuffix


def one():
    return 1


def onedict():
    return defaultdict(one)


def calACS(a, b):
    m = len(a)
    n = len(b)
    N = defaultdict(one)

    for i in xrange(1, m):
        for j in xrange(1, n):
            if a[i] == b[j]:
                N[i, j] = N[i-1, j-1] * 2
            else:
                N[i, j] = N[i-1, j] + N[i, j-1] - N[i-1, j-1]
    return N[m-1, n-1]

def acs(a, b):
    together = u''.join([a, '$', b])