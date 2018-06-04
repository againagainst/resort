import json
import pathlib
from typing import Type

from etalons import BaseEtalon, BasicHTTPResponseEtalon
from errors import BadProjectPath, EtalonPathError


class EtalonIO:
    """File system layer. Reads/writes etalons.

    Args:
        project_dir (pathlib.Path): project directory
        make_dir [bool, False]: If True, resort won't complain
        about missing directories, but try to create them.

    Raises:
        NotADirectoryError: if :project_dir: is a file
    """
    def __init__(self, project_dir: pathlib.Path, make_dir=False):
        if project_dir.exists() and not project_dir.is_dir():
            raise BadProjectPath(project_dir)
        if make_dir:
            project_dir.mkdir(parents=True, exist_ok=True)
        self.project_dir = project_dir

    def save(self, etalon: BaseEtalon):
        """Writes :etalon: to the file

        Args:
          etalon: BaseEtalon
        """
        etadir = self.project_dir.joinpath(etalon.dir)
        etapath = self.project_dir.joinpath(etalon.path)

        etadir.mkdir(parents=True, exist_ok=True)
        with etapath.open(mode='w') as f:
            json.dump(etalon.dump(), f, indent=2)

    def read(self, entry: str, Etalon: Type[BaseEtalon]=BasicHTTPResponseEtalon):
        """Reads etalon identified by :entry: from it's file.

        Args:
            entry (str): API entry from server spec
            Etalon: Constructor (Default is BasicHTTPResponseEtalon)

        Returns:
            Etalon: object
        """

        etalon = Etalon(entry=entry)
        etapath = self.project_dir.joinpath(etalon.path)

        try:
            with etapath.open(mode='r') as f:
                etalon.restore_from_dict(json.load(f))
        except FileNotFoundError:
            raise EtalonPathError(entry)
        return etalon
