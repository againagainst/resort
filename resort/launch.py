import options
import etalons

from base_client import BasicClient
from basic_rest_def import PingEntry


def basic_etalon_saving_example():
    opts = options.read_all()
    ping_entry = PingEntry(opts['server']['url'])
    response = ping_entry.read()
    etalon = etalons.BasicHTTPResponseEtalon(response)
    eio = etalons.EtalonIO(output_dir=opts['output'], make_dir=True)
    eio.save(etalon)


def schema_request_etalon_saving_example():
    opts = options.read_all()
    client = BasicClient(server_url=opts['server']['url'],
                         schema_file=opts['server']['schema']
                         ).prepare()
    eio = etalons.EtalonIO(output_dir=opts['output'], make_dir=True)
    for etalon in client.fetch_etalons():
        eio.save(etalon)


if __name__ == '__main__':
    schema_request_etalon_saving_example()
