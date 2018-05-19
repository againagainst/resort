import json
import re
import pathlib


class ServerSpecReader(object):
    ENTRY_PREFIX = re.compile(r'^(/)')

    def __init__(self, spec_file):
        self._file = spec_file
        self._paths = None
        self.version = None
        self.vprefix = None

    def prepare(self):
        with open(self._file) as fp:
            body = json.load(fp)
            self._paths = body['paths']
            self.version = body['info']['version']
            self.vprefix = pathlib.Path('v' + self.version)
        return self

    def paths(self):
        for full_entry in self._paths.keys():
            # '/ping/12' -> 'ping/12'
            yield self.ENTRY_PREFIX.sub('', full_entry)

    def paths_and_methods(self):
        for full_entry, entry_desc in self._paths.items():
            # '/ping/12' -> 'ping/12'
            relative_entry = self.ENTRY_PREFIX.sub('', full_entry)
            for method in entry_desc.keys():
                yield method, relative_entry
