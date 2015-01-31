import functools
import inspector

class memoize:
  def __init__(self, function):
    self.function = function
    self.memoized = {}

  def __call__(self, *args):
    try:
        return self.memoized[args]
    except KeyError:
        self.memoized[args] = self.function(*args)
        return self.memoized[args]


def vectorize(fn):
    """
    Allows a function to accept one or more values, 
    but internally deal only with a single item, 
    and returning a list or a single item depending
    on what is desired.
    """
    @functools.wraps(fn)
    def vectorized_fn(values, *vargs, **kwargs):
        wrap = not isinstance(values, (list, tuple))
        should_unwrap = not kwargs.get('wrap', False)
        unwrap = wrap and should_unwrap
        
        if wrap:
            values = [values]
        
        results = [fn(value, *vargs, **kwargs) for value in values]

        if unwrap:
            results = results[0]

        return results

        
def immutable(method):
    @inspector.wraps(method)
    def wrapped_method(self, *vargs, **kwargs):
        obj = self.clone()
        method(obj, *vargs, **kwargs)
        return obj

    return wrapped_method


def identity(value):
    return value


def soak(*vargs, **kwargs):
    pass