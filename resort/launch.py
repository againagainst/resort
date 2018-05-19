import options
import etalons

from base_client import BasicClient


def schema_request_etalon_saving_example():
    opts = options.read_all()
    assert opts['mode'] == 'store'
    client = BasicClient(server_url=opts['server']['url'],
                         spec_file=opts['server']['spec']
                         ).prepare()
    eio = etalons.EtalonIO(project_dir=opts['project'], make_dir=True)
    for etalon in client.fetch_etalons():
        eio.save(etalon)


def schema_request_etalon_reading_example():
    opts = options.read_all()
    assert opts['mode'] == 'check'
    etalons.EtalonIO(project_dir=opts['project'], make_dir=True)


if __name__ == '__main__':
    schema_request_etalon_saving_example()
