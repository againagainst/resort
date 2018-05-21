import pathlib
import requests
import json


class BasicHTTPResponseEtalon:
    __STR__ = '''
    Response:
    {headers}
    Body:
    {body}
    '''

    def __init__(self, entry: str, response: requests.Response=None, name: str=None):
        """TODO: Add the docstring

        Args:
            entry (str): [description]
            response (requests.Response, optional): Defaults to None. [description]
            name (str, optional): Defaults to None. [description]
        """

        self._entry = entry
        self._name = name or 'etalon'
        if response is not None:
            self._headers = response.headers
            self._body = response.text

    def restore_from_dict(self, etalon: dict):
        """TODO: Add the docstring

        Args:
          etalon: dict:

        Returns:

        """
        self._headers = etalon['headers']
        self._body = etalon['body']

    @property
    def name(self):
        return self._name

    @property
    def dir(self):
        return pathlib.Path(self._entry)

    @property
    def path(self):
        return self.dir.joinpath("{0}.json".format(self.name))

    def dump(self):
        """TODO: Add the docstring

        Returns:
            [type]: [description]
        """

        return dict(headers=dict(self._headers),
                    body=self._body)

    def __str__(self):
        return BasicHTTPResponseEtalon.__STR__.format(
            headers="\n".join('{0}: {1}'.format(k, v) for k, v in self._headers.items()),
            body=self._body)


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

    def save(self, etalon: BasicHTTPResponseEtalon):
        """TODO: Add the docstring

        Args:
          etalon: BasicHTTPResponseEtalon:

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
