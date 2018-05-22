from pprint import pprint

from dictdiffer import diff

import options
import etalons

from base_client import BasicClient
from server_spec import ServerSpecReader


def store_example(opts: dict):
    assert opts['mode'] == 'store'
    client = BasicClient(server_url=opts['server']['url'],
                         spec_file=opts['server']['spec']
                         ).prepare()
    eio = etalons.EtalonIO(project_dir=opts['project'], make_dir=True)
    for etalon in client.snapshot_etalons():
        eio.save(etalon)


def checking_example(opts: dict):
    """TODO: Add the docstring
    """
    assert opts['mode'] == 'check'
    spec_reader = ServerSpecReader(opts['server']['spec']).prepare()
    client = BasicClient(server_url=opts['server']['url'])
    eio = etalons.EtalonIO(project_dir=opts['project'])
    for method, entry in spec_reader.paths_and_methods():
        etalon_d = eio.read(entry).dump()
        snap_d = client.snapshot(entry, method).dump()
        pprint(list(diff(etalon_d, snap_d)))


def reading_example(opts: dict):
    """TODO: Add the docstring
    """
    assert opts['mode'] == 'check'
    eio = etalons.EtalonIO(project_dir=opts['project'])
    spec_reader = ServerSpecReader(opts['server']['spec']).prepare()
    for entry in spec_reader.paths():
        eta = eio.read(entry)
        print(eta)


if __name__ == '__main__':
    opts = options.read_all()
    if opts['mode'] == 'store':
        store_example(opts)
    else:
        checking_example(opts)
