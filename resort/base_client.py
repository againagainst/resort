import urllib.parse

import requests

from etalons import BasicHTTPResponseEtalon
from server_spec import ServerSpecReader


class BasicClient(object):

    def __init__(self, server_url: str, spec_file: str=None):
        self._server_url = server_url
        if spec_file is not None:
            self.server_spec = ServerSpecReader(spec_file=spec_file)

    def prepare(self):
        '''
        Load a API Spec to the client's ServerSpecReader.
        returns self to create a prepared client:
        client = BasicClient().prepare()
        '''
        self.server_spec.prepare()
        return self

    def snapshot_etalons(self, Etalon=BasicHTTPResponseEtalon):
        for method, each_entry in self.server_spec.paths_and_methods():
            yield self.snapshot(each_entry, method)

    def snapshot(self, entry: str, method: str, Cls=BasicHTTPResponseEtalon):
        url = urllib.parse.urljoin(self._server_url, entry)
        return Cls(entry=entry,
                   response=requests.request(method, url))
