import daiquiri

import etalons
from client import BasicClient
from server_spec import ServerSpecReader
from project import ResortProject

LOG = daiquiri.getLogger(__name__)


class ResortEngine:

    @staticmethod
    def store(project: ResortProject, opts: dict):
        """TODO: Add description docstring

        Args:
            opts (dict): [description]
        """
        for each_test in opts['tests']:
            client = BasicClient.prepare(spec_file=each_test)
            eio = etalons.EtalonIO(project_dir=opts['project'], make_dir=True)
            for etalon in client.snapshot_etalons():
                eio.save(etalon)

    @staticmethod
    def check(project: ResortProject, opts: dict):
        """TODO: Add description docstring

        Args:
            opts (dict): [description]
        """
        raise NotImplementedError()  # TODO cheking
        # spec_reader = ServerSpecReader(opts['server']['spec']).prepare()
        # client = BasicClient(server_url=opts['server']['url'])
        # differ = etalons.BaseComparator(ignored={'headers.Date'})
        # eio = etalons.EtalonIO(project_dir=opts['project'])
        # for method, entry in spec_reader.paths_and_methods():
        #     result = differ.check(eio.read(entry), client.snapshot(entry, method))
        #     # pprint(list(diff(etalon_d, snap_d, ignore={'headers.Date'})))
        #     print('{0}:'.format(entry))
        #     print(result)
