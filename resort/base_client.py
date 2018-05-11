import json
import urllib.parse

import requests

from etalons import BasicHTTPResponseEtalon


class BasicClient(object):

    def __init__(self, server_url, schema_info):
        '''
        schema_info = {
            'type' = 'file',
            'file' = './path/to/schema,
        }
        '''
        self._type = schema_info.get('type', 'file')
        self._file = schema_info.get('file', None)
        self._server_url = server_url

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
        if self._type == 'file':
            with open(self._file) as fp:
                self._schema_body = BasicClient.parse_schema(fp)
        return self

    def fetch_etalons(self, http_methods=('GET',), Etalon=BasicHTTPResponseEtalon):
        for url in self.paths():
            for METHOD in http_methods:
                _, _, entry, _, _ = urllib.parse.urlsplit(url)
                yield Etalon(requests.request(METHOD, url), name=entry.replace('/', '-'))

    def paths(self, schema=None):
        schema = schema or self._schema_body
        for each_path in schema.keys():
            yield urllib.parse.urljoin(self._server_url, each_path)
