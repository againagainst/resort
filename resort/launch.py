from pprint import pprint

import options
import etalons

from base_client import BasicClient
from basic_rest_def import PingEntry


def basic_etalon_saving_example():
    opts = options.read_all()
    ping_entry = PingEntry(opts['server'])
    response = ping_entry.read()
    etalon = etalons.BasicHTTPResponseEtalon(response)
    eio = etalons.EtalonIO(opts)
    eio.save(etalon, opts.get('output'))


def schema_request_etalon_saving_example():
    opts = options.read_all()
    # TODO: init from opts
    client = BasicClient(server_url=opts['server'],
                         schema_info={'file': opts['schema']}
                         ).prepare()
    eio = etalons.EtalonIO(opts)
    for etalon in client.fetch_etalons():
        eio.save(etalon)


if __name__ == '__main__':
    schema_request_etalon_saving_example()
