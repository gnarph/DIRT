def memoize_single_arg(f):
    """
    Memoiztion decorator for functions (not methods) that take a
    single parameter
    """
    class Memodict(dict):
        __slots__ = ()

        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret
    return Memodict().__getitem__