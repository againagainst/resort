import pathlib
import requests


class BasicHTTPResponseEtalon:
    '''
    Response
    HTTP/1.1 200 OK
    Etag: "0e514a0662bcb69dc863953d1ce26e3d40e81a87"
    Content-Type: text/html; charset=UTF-8
    Date: Sat, 05 May 2018 11:19:21 GMT
    Content-Length: 4
    Server: TornadoServer/5.0.2
    '''

    def __init__(self, entry: str, response: requests.Response, name: str=None):
        self._entry = entry
        self._headers = response.headers
        self._body = response.text
        self._name = name or 'etalon'

    @property
    def name(self):
        return self._name

    @property
    def dir(self):
        return pathlib.Path(self._entry)
    
    @property
    def path(self):
        return self.dir.joinpath("{0}.str".format(self.name))

    def __str__(self):
        return '''Response:
{headers}
Body:
{body}
'''.format(headers="\n".join('{0}: {1}'.format(k, v)
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
            f.write(str(etalon))
