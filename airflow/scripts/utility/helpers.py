from functools import wraps
from time import time
from .logger import logger

def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        # print('Function :%r with args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts))
        logger.info('Function :%r with args:[ %r] took: %2.4f sec' % (f.__name__, kw, te-ts))
        return result
    return wrap