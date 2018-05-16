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

    def __init__(self, response: requests.Response, name: str=''):
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

    def __init__(self, output_dir, mkdir=False):
        if output_dir.exists() and not output_dir.is_dir():
            raise NotADirectoryError(output_dir)
        self.output_dir = output_dir
        if mkdir:
            self.output_dir.mkdir(exist_ok=True)

    def save(self, etalon: BasicHTTPResponseEtalon, filepath: pathlib.Path=None, mkdir=False):
        if filepath is None:
            filename = '{0}.etalon'.format(etalon.name or 'unknown')
            filepath = self.output_dir.joinpath(filename)

        with filepath.open(mode='w') as f:
            f.write(str(etalon))
            pass
        pass
