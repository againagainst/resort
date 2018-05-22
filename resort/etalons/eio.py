import json
import pathlib

from etalons import BaseEtalon, BasicHTTPResponseEtalon


class EtalonIO:
    """TODO: Add the classdoc string
    """

    def __init__(self, project_dir: pathlib.Path, make_dir=False):
        """TODO: Add the docstring

        Args:
            project_dir (pathlib.Path): [description]
            make_dir (bool, optional): Defaults to False. [description]

        Raises:
            NotADirectoryError: [description]
        """
        if project_dir.exists() and not project_dir.is_dir():
            raise NotADirectoryError(project_dir)
        if make_dir:
            project_dir.mkdir(parents=True, exist_ok=True)
        self.project_dir = project_dir

    def save(self, etalon: BaseEtalon):
        """TODO: Add the docstring

        Args:
          etalon: BaseEtalon:

        Returns:

        """
        etadir = self.project_dir.joinpath(etalon.dir)
        etapath = self.project_dir.joinpath(etalon.path)

        etadir.mkdir(parents=True, exist_ok=True)
        with etapath.open(mode='w') as f:
            json.dump(etalon.dump(), f, indent=2)

    def read(self, entry: str, Etalon=BasicHTTPResponseEtalon):
        """TODO: Add the docstring

        Args:
          entry: str:
          Etalon:  (Default value = BasicHTTPResponseEtalon)

        Returns:

        """
        etalon = Etalon(entry=entry)
        etapath = self.project_dir.joinpath(etalon.path)

        with etapath.open(mode='r') as f:
            etalon.restore_from_dict(json.load(f))
        return etalon
