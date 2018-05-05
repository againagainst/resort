import requests


def methods(*http_methods):
    '''
    '''
    def real_decorator(operation):
        def wrapper(*args, **kwargs):
            self = args[0]
            url = "{server}/{url}".format(server='http://localhost:8888', url=self.url)
            for METHOD in http_methods:
                response = requests.request(METHOD, url)
                kwargs['response'] = response
                result = operation(*args, **kwargs)
            return result
        return wrapper
    return real_decorator
