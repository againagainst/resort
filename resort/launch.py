from pprint import pprint

import options
import etalons

from base_client import BasicClient
from basic_rest_def import PingEntry


def basic_etalon_saving_example():
    opts = options.read_all()
    ping_entry = PingEntry(opts['input'])
    response = ping_entry.read()
    etalon = etalons.BasicHTTPResponseEtalon(response)
    eio = etalons.EtalonIO(opts)
    eio.save(etalon, opts.get('output'))


def schema_request_etalon_saving_example():
    opts = options.read_all()
    client = BasicClient(dict(file=opts['input'])).prepare()
    pprint(client.schema_body)


if __name__ == '__main__':
    schema_request_etalon_saving_example()
