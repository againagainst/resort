import requests

import etalons


class MIMETypeEtalon(etalons.BaseEtalon):
    """Changes self behavior according to a MIME type
    of the response.

    text/html -- str
    application/json -- json dumps/loads
    """
    _EXT = "json"

    def __init__(self, entry: str, response: requests.Response=None):
        super().__init__(entry=entry, ext=MIMETypeEtalon._EXT)
