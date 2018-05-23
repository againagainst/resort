import json
import re
import pathlib


class ServerSpecReader(object):
    """Allows to iterate over a server specification

    Args:
        spec_file (pathlib.Path): a full path to a spec file
    """
    ENTRY_PREFIX = re.compile(r'^(/)')

    def __init__(self, spec_file):
        self._file = spec_file
        self._paths = None
        self.version = None
        self.vprefix = None

    def prepare(self):
        """Reads the specification from the spec_file.
        TODO: separate spec version and resort's project version
        TODO: make a static constructor

        Returns: self to create a prepared client
            self: spec = ServerSpecReader().prepare()
        """

        with open(self._file) as fp:
            body = json.load(fp)
            self._paths = body['paths']
            self.version = body['info']['version']
            self.vprefix = pathlib.Path('v' + self.version)
        return self

    def paths(self):
        """Yields each entry in the spec.

        Returns:
          a generator of paths: str
        """
        for full_entry in self._paths.keys():
            # '/ping/12' -> 'ping/12'
            yield self.ENTRY_PREFIX.sub('', full_entry)

    def paths_and_methods(self):
        """Yields each (method, path) for each entry in the spec.

        Returns:
          a generator of method, path: tuple
        """
        for full_entry, entry_desc in self._paths.items():
            # '/ping/12' -> 'ping/12'
            relative_entry = self.ENTRY_PREFIX.sub('', full_entry)
            for method in entry_desc.keys():
                yield method, relative_entry
