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

    def __init__(self, response: requests.Response):
        self._headers = response.headers

    def __str__(self):
        title = 'Response'
        content = "\n".join('{0}: {1}'.format(k, v) for k, v in self._headers.items())
        return '{title}\n{content}'.format(title=title, content=content)


class EtalonIO:

    def __init__(self, config: dict):
        self.read_file = config.get('input')
        self.write_file = config.get('output')

    def save(self, etalon: BasicHTTPResponseEtalon, filepath: pathlib.Path=None):
        filepath = filepath or self.write_file

        with filepath.open(mode='w') as f:
            f.write(str(etalon))
            pass
        pass
