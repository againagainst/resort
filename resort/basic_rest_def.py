from urls import methods


class PingEntry():
    url = r'ping'

    @methods('GET')
    def read(self, response=None):
        print("It works!")
        print(response)
