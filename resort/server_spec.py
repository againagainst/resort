import json
import pathlib

from . import errors


class ServerSpecReader(object):
    """Allows to iterate over a server specification

    Args:
        spec_file (pathlib.Path): a full path to a spec file
    """
    __supported_auth_methods = ('post-request')

    def __init__(self):
        self._file = None
        self.paths = None
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
            try:
                body = json.load(fp)
                reader.paths = ServerSpecReader.ensure_params(body['paths'])
                reader.url = body['server']['url']
                reader.session = ServerSpecReader.parse_session(body)
                info_title = body["info"].get("title", None)
                reader.test_name = info_title or reader._file.stem
                reader.version = body['info']['version']
                reader.vprefix = pathlib.Path('v' + reader.version)
            except KeyError as err:
                raise errors.SpecFormatError(fname=reader._file,
                                             err=err,
                                             reason='section is required')
        return reader

    def fetch_signatures(self):
        """Yields method, path, payload for each entry in the spec.

        Returns:
          a generator of method, path: tuple
        """

        for entry_id, (uri, params) in enumerate(self.paths):
            yield entry_id, uri, params

    def make_name(self, entry_id):
        return "{0}_{1}".format(self.test_name, entry_id)

    @property
    def has_session(self):
        return self.session is not None

    @property
    def session_type(self):
        return self.session['type'] if self.has_session else None

    @classmethod
    def parse_session(cls, body: dict):
        try:
            session_desc = body['server']['session']
            if 'create' in session_desc and len(session_desc['create']) == 1:
                session_desc['create'].append(dict())
            if 'delete' in session_desc and len(session_desc['delete']) == 1:
                session_desc['delete'].append(dict())
        except KeyError:
            return None

        return session_desc

    @classmethod
    def ensure_params(cls, request_signatures):
        return [(x[0], x[1]) if len(x) > 1 else (x[0], dict()) for x in request_signatures]
