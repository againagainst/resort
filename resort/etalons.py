import pathlib
import requests
import json


class BasicHTTPResponseEtalon:

    def __init__(self, entry: str, response: requests.Response=None, name: str=None):
        self._entry = entry
        self._name = name or 'etalon'
        if response is not None:
            self._headers = response.headers
            self._body = response.text

    @property
    def name(self):
        return self._name

    @property
    def dir(self):
        return pathlib.Path(self._entry)

    @property
    def path(self):
        return self.dir.joinpath("{0}.json".format(self.name))

    def dump(self, fp):
        output = dict(headers=dict(self._headers),
                      body=self._body)
        return json.dump(output, fp, indent=2)

    def load(self, fp):
        etalon = json.load(fp)
        self._headers = etalon['headers']
        self._body = etalon['body']

    __STR = '''Response:
{headers}
Body:
{body}
'''

    def __str__(self):
        return self.__STR.format(headers="\n".join('{0}: {1}'.format(k, v)
                                                   for k, v in self._headers.items()),
                                 body=self._body
                                 )


class EtalonIO:

    def __init__(self, project_dir: pathlib.Path, make_dir=False):
        if project_dir.exists() and not project_dir.is_dir():
            raise NotADirectoryError(project_dir)
        if make_dir:
            project_dir.mkdir(parents=True, exist_ok=True)
        self.project_dir = project_dir

    def save(self, etalon: BasicHTTPResponseEtalon):
        etadir = self.project_dir.joinpath(etalon.dir)
        etapath = self.project_dir.joinpath(etalon.path)

        etadir.mkdir(parents=True, exist_ok=True)
        with etapath.open(mode='w') as f:
            etalon.dump(f)

    def read(self, entry: str, Etalon=BasicHTTPResponseEtalon):
        etalon = Etalon(entry=entry)
        etapath = self.project_dir.joinpath(etalon.path)

        with etapath.open(mode='r') as f:
            etalon.load(f)
        return etalon
