import json
import re


class ServerSpecReader(object):
    ENTRY_PREFIX = re.compile(r'^(/)')

    def __init__(self, spec_file):
        self._file = spec_file
        self.schema_body = None

    @classmethod
    def parse_schema(self, in_file):
        body = json.load(in_file)
        return body['paths']

    def prepare(self):
        with open(self._file) as fp:
            self.schema_body = ServerSpecReader.parse_schema(fp)

    def paths(self, server_spec=None):
        server_spec = server_spec or self.schema_body
        for full_entry in server_spec.keys():
            # '/ping/12' -> 'ping/12'
            yield self.ENTRY_PREFIX.sub('', full_entry)
