import requests

from .base import BaseEtalon


class BasicHTTPResponseEtalon(BaseEtalon):
    """Basic etalon, represents a requests.Response as json:
    ```
    {
      "headers": {"Header": "Value"
                  ...
                 },
      "body": ...
    }
    ```
    name: test_name_N_basic.et.json

    Args:
        entry (str): - spec entry.
        response [requests.Response, None]
    """
    _EXT = 'json'
    _STR = 'Response:\n{headers}\nBody:\n{body}'

    def __init__(self, entry: str, name: str=None,
                 response: requests.Response=None, **kwargs):
        super().__init__(entry=entry,
                         name="{name}_basic".format(name=name),
                         ext=BasicHTTPResponseEtalon._EXT,
                         **kwargs)
        if response is not None:
            self._headers = response.headers
            self._body = response.text

    def restore_from_dict(self, etalon: dict):
        """Restores etalon object from the JSON-like object.
        TODO: rename to `load`

        Args:
          etalon: dict
        """
        self._headers = etalon['headers']
        self._body = etalon['body']

    def dump(self):
        """JSON-like representation of the object.

        Returns:
            dict: representation of the object
        """
        return dict(headers=dict(self._headers),
                    body=self._body)

    def __str__(self):
        strargs = dict(headers="\n".join('{0}: {1}'.format(k, v)
                                         for k, v
                                         in self._headers.items()),
                       body=self._body)
        return BasicHTTPResponseEtalon._STR.format(strargs)
