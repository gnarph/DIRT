def memoize_many_args(func):
    """
    Memoization decorator for functions taking one or more arguments.
    """
    class memodict(dict):
        def __init__(self, f):
            self.f = f

        def __call__(self, *args):
            return self[args]

        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(func)


def memoize_single_arg(f):
    """
    Memoiztion decorator for functions (not methods) that take a
    single parameter
    """
    class memodict(dict):
        __slots__ = ()

        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret
    return memodict().__getitem__