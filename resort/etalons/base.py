import re


class BaseEtalon(object):
    ENTRY_PREFIX = re.compile(r'^(/)')

    def __init__(self, entry: str, name: str=None, ext: str='txt'):
        """Base class for all etalons. Represents a link between
        entry in the spec and it's path in the snapshots directory

        Args:
            entry (str): Entry path (actually an URI)
            name [str, 'etalon']: File Name
            ext [str, 'txt']: File extension
        """
        self._entry = BaseEtalon.sub_entry(entry)
        self._name = name or self._entry
        self._ext = ext

    @property
    def entry(self):
        """unified name of a resource (uri) which the snapshot represents"""
        return self._entry

    @property
    def name(self):
        """name of the snapshot, like test_name_N_etalontype"""
        return self._name

    @property
    def ext(self):
        """extension of the snapshot, defaults to .txt"""
        return self._ext

    @property
    def file_name(self):
        """actual name of the snapshot file"""
        return "{0}.et.{1}".format(self.name, self.ext)

    @staticmethod
    def encode_filepath(url: str):
        return url.replace('/', ' ')

    @staticmethod
    def decode_filepath(path: str):
        return path.replace(' ', '/')

    @classmethod
    def sub_entry(cls, urn: str):
        """'/ping/12' -> 'ping/12'"""
        return cls.ENTRY_PREFIX.sub('', urn)
