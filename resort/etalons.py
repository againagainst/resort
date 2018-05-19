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

    def __init__(self, response: requests.Response, name: str=None):
        self._headers = response.headers
        self._name = name

    @property
    def name(self):
        return self._name

    def __str__(self):
        title = 'Response'
        content = "\n".join('{0}: {1}'.format(k, v) for k, v in self._headers.items())
        return '{title}\n{content}'.format(title=title, content=content)


class EtalonIO:

    def __init__(self, project_dir: pathlib.Path, make_dir=False):
        if project_dir.exists() and not project_dir.is_dir():
            raise NotADirectoryError(project_dir)
        if make_dir:
            project_dir.mkdir(parents=True, exist_ok=True)
        self.project_dir = project_dir

    def save(self, etalon: BasicHTTPResponseEtalon):
        filename = '{0}.etalon'.format(etalon.name or 'unknown')
        filepath = self.project_dir.joinpath(filename)

        with filepath.open(mode='w') as f:
            f.write(str(etalon))
