import json
import pathlib


class ServerSpecReader(object):
    """Allows to iterate over a server specification

    Args:
        spec_file (pathlib.Path): a full path to a spec file
    """

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

        with self._file.open() as fp:
            body = json.load(fp)
            self._paths = self.add_none_payload(body['paths'])
            self.url = body['server']['url']
            self.test_name = body["info"]["title"]
            self.version = body['info']['version']
            self.vprefix = pathlib.Path('v' + self.version)
        return self

    def add_none_payload(self, paths: list):
        """[["/index.html", "get"], ["/api/user", "post", {...}]] ->
        [["/index.html", "get", None], ["/api/user", "post", {...}]]
        So you can unpack them.

        Args:
            paths (list): [list of test entries]
        """
        for entry in paths:
            if len(entry) == 2:
                entry.append(None)
        return paths

    def paths(self):
        """Yields each entry in the spec.

        Returns:
          a generator of paths: str
        """
        for entry, _, _ in self._paths:
            yield entry[0]

    def paths_and_methods(self):
        """Yields each (method, path) for each entry in the spec.

        Returns:
          a generator of method, path: tuple
        """
        for entry, method, payload in self._paths:
            yield method, entry
