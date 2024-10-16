from functools import wraps
from time import time

def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        # print('Function :%r with args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts))
        print('Function :%r with args:[ %r] took: %2.4f sec' % (f.__name__, kw, te-ts))
        return result
    return wrap