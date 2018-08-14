import re
import pathlib


class BaseEtalon(object):
    ENTRY_PREFIX = re.compile(r'^(/)')

    def __init__(self, entry: str, name: str=None, ext: str='txt'):
        """Base class for all etalons. Represents a link between
        entry in the spec and it's path in the snapshots directory

        Args:
            entry (str): Entry path
            name [str, 'etalon']: File Name
            ext [str, 'txt']: File extension
        """
        self._entry = BaseEtalon.sub_entry(entry)
        self._name = name or self._entry
        self._ext = ext

    @property
    def entry(self):
        return self._entry

    @property
    def name(self):
        return self._name

    @property
    def ext(self):
        """File extension, defaults to .txt"""
        return self._ext

    @property
    def file_name(self):
        """
        [up to eio/client][up to self.dir][to be returned]:
        /path/project_dir/ etalons/        test_name_etalon.fmt

        Returns:
            [str]: name of the etalon file: test_title+.extension
        """
        return "{0}.et.{1}".format(self._name, self._ext)

    @property
    def path(self):
        """
        [up to eio/client][dir+file_name, to be returned]:
        /path/project_dir/ etalons/test_name_etalon.fmt

        Returns:
            [pathlib.Path]: path to the etalon, relative to the project_dir
        """
        return self.dir.joinpath(self.file_name)

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
