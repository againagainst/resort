import options
import etalons

from base_client import BasicClient


def schema_request_etalon_saving_example():
    opts = options.read_all()
    client = BasicClient(server_url=opts['server']['url'],
                         schema_file=opts['server']['schema']
                         ).prepare()
    eio = etalons.EtalonIO(project_dir=opts['project'], make_dir=True)
    for etalon in client.fetch_etalons():
        eio.save(etalon)


if __name__ == '__main__':
    schema_request_etalon_saving_example()
