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

def unicode_error_handler(fn):
    def wrapped(*args, **kwargs):
        try:
            val = fn(*args, **kwargs)
        except UnicodeDecodeError as e:
            tmpl = u'Error {err} in {func_name} with args {args},{kwargs}'
            msg = tmpl.format(err=str(e),
                              func_name=str(fn),
                              args=args,
                              kwargs=kwargs)
            print msg
            raise
        return val
    return wrapped
