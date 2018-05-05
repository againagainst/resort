from urls import methods
from etalons import BasicHTTPResponseEtalon


class PingEntry():
    url = r'ping'

    @methods('GET')
    def read(self, response=None):
        return response

    @methods('GET')
    def store_get_etalon(self, response=None):
        etalon = BasicHTTPResponseEtalon(response)
        print(str(etalon))
