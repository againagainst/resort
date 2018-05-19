import json
import re
import urllib.parse

import requests

from etalons import BasicHTTPResponseEtalon


class BasicClient(object):
    ENTRY_PREFIX = re.compile(r'^(/)')

    def __init__(self, server_url, schema_file):
        '''
        '''
        self._server_url = server_url
        self._file = schema_file

    @property
    def schema_body(self):
        return self._schema_body

    @classmethod
    def parse_schema(self, in_file):
        body = json.load(in_file)
        return body['paths']

    def prepare(self):
        '''
        Load a schema to the client.
        returns self to create a prepared client:
        client = BasicClient().prepare()
        '''
        with open(self._file) as fp:
            self._schema_body = BasicClient.parse_schema(fp)
        return self

    def fetch_etalons(self, http_methods=('GET',), Etalon=BasicHTTPResponseEtalon):
        for each_entry in self.paths():
            url = urllib.parse.urljoin(self._server_url, each_entry)
            for METHOD in http_methods:
                yield Etalon(entry=each_entry,
                             response=requests.request(METHOD, url))

    def paths(self, schema=None):
        schema = schema or self._schema_body
        for full_entry in schema.keys():
            # '/ping/12' -> 'ping/12'
            yield self.ENTRY_PREFIX.sub('', full_entry)
