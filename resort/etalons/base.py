import re
import pathlib


class BaseEtalon(object):
    ENTRY_PREFIX = re.compile(r'^(/)')

    def __init__(self, entry: str, name: str='etalon', ext: str='txt'):
        """Base class for all etalons. Represents a link between
        entry in the spec and it's path in the snapshots directory

        Args:
            entry (str): Entry path
            name [str, 'etalon']: File Name
            ext [str, 'txt']: File extension
        """
        # '/ping/12' -> 'ping/12'
        self._entry = self.ENTRY_PREFIX.sub('', entry)
        self._name = name
        self._ext = ext

    @property
    def name(self):
        return self._name

    @property
    def ext(self):
        return self._ext

    @property
    def file_name(self):
        return "{0}.{1}".format(self._name, self._ext)

    @property
    def dir(self):
        return pathlib.Path(self._entry)

    @property
    def path(self):
        return self.dir.joinpath(self.file_name)
