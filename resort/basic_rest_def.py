from urls import methods


class PingEntry():
    entity = r'ping'

    def __init__(self, remote: str):
        self.remote = remote

    @property
    def url(self):
        return "{server}/{url}".format(server=self.remote, url=self.entity)

    @methods('GET')
    def read(self, response=None):
        return response
