import json
import pathlib


class ServerSpecReader(object):
    """Allows to iterate over a server specification

    Args:
        spec_file (pathlib.Path): a full path to a spec file
    """

    def __init__(self):
        self._file = None
        self._paths = None
        self.version = None
        self.vprefix = None

    @classmethod
    def prepare(cls, spec_file: pathlib.Path):
        """Reads the specification from the spec_file.
        TODO: separate spec version and resort's project version

        Returns: self to create a prepared client
            self: spec = ServerSpecReader.prepare()
        """
        reader = cls()
        reader._file = spec_file

        with reader._file.open() as fp:
            body = json.load(fp)
            reader._paths = reader.ensure_payload(body['paths'])
            reader.url = body['server']['url']
            # reader.test_name = body["info"].get("title", None)
            reader.version = body['info']['version']
            reader.vprefix = pathlib.Path('v' + reader.version)
        return reader

    def ensure_payload(self, paths: list):
        """Converts
        [["/index.html", "get"], ["/api/user", "post", {...}]]
        to
        [["/index.html", "get", None], ["/api/user", "post", {...}]]
        So it's easier to unpack them.

        Args:
            paths (list): [list of test entries]
        """
        return list(entry if len(entry) == 3 else entry + [None] for entry in paths)

    def paths(self):
        """Yields method, path, payload for each entry in the spec.

        Returns:
          a generator of method, path: tuple
        """
        for entry, method, payload in self._paths:
            yield method, entry, payload
