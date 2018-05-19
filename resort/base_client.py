import urllib.parse

import requests

from etalons import BasicHTTPResponseEtalon
from server_spec import ServerSpecReader


class BasicClient(object):

    def __init__(self, server_url, spec_file):
        '''
        '''
        self.server_spec = ServerSpecReader(spec_file=spec_file)
        self._server_url = server_url

    def prepare(self):
        '''
        Load a API Spec to the client's ServerSpecReader.
        returns self to create a prepared client:
        client = BasicClient().prepare()
        '''
        self.server_spec.prepare()
        return self

    def fetch_etalons(self, http_methods=('GET',), Etalon=BasicHTTPResponseEtalon):
        for each_entry in self.server_spec.paths():
            url = urllib.parse.urljoin(self._server_url, each_entry)
            for METHOD in http_methods:
                yield Etalon(entry=each_entry,
                             response=requests.request(METHOD, url))
