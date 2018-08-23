import json
import pathlib


class ServerSpecReader(object):
    """Allows to iterate over a server specification

    Args:
        spec_file (pathlib.Path): a full path to a spec file
    """
    __supported_auth_methods = ('post-request')

    def __init__(self):
        self._file = None
        self.requests = None
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
            reader.requests = body['requests']
            reader.host = body['server']['host']
            reader.session = reader.get_session(body)
            info_title = body["info"].get("title", None)
            reader.test_name = info_title or reader._file.stem
            reader.version = body['info']['version']
            reader.vprefix = pathlib.Path('v' + reader.version)
        return reader

    def fetch_signatures(self):
        """Yields method, path, payload for each entry in the spec.

        Returns:
          a generator of method, path: tuple
        """
        for entry_id, (uri, params) in enumerate(self.requests):
            yield entry_id, uri, params

    def make_name(self, entry_id):
        return "{0}_{1}".format(self.test_name, entry_id)

    @classmethod
    def get_session(cls, body: dict):
        try:
            session_desc = body['server']['session']
        except KeyError:
            return None

        auth_method = session_desc.get('type', 'post-request')
        if auth_method not in ServerSpecReader.__supported_auth_methods:
            raise NotImplementedError

        return session_desc
