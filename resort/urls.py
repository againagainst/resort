import requests
from functools import wraps


def request_for_methods(*http_methods):
    """TODO: Add the docstring

    Args:
      *http_methods:

    Returns:

    """
    def real_decorator(operation):
        @wraps(operation)
        def wrapper(*args, **kwargs):
            self = args[0]
            for METHOD in http_methods:
                response = requests.request(METHOD, self.url)
                kwargs['response'] = response
                result = operation(*args, **kwargs)
            return result
        return wrapper
    return real_decorator
