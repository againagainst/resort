import daiquiri

import etalons
from client import BasicClient
from server_spec import ServerSpecReader
from project import ResortProject

LOG = daiquiri.getLogger(__name__)


class ResortEngine:

    @staticmethod
    def store(project: ResortProject):
        for each_test in project.test_specs:
            LOG.info('Storing: ' + str(each_test))
            spec_reader = ServerSpecReader.prepare(spec_file=each_test)
            client = BasicClient(spec_reader)
            eio = etalons.EtalonIO(project_dir=project.project_dir, make_dir=True)
            for etalon in client.snapshot_etalons():
                eio.save(etalon)

    @staticmethod
    def check(project: ResortProject):
        for each_test in project.test_specs:
            spec_reader = ServerSpecReader.prepare(spec_file=each_test)
            client = BasicClient(spec_reader)
            differ = etalons.BaseComparator(ignored=project.ignored)
            eio = etalons.EtalonIO(project_dir=project.project_dir)
            for method, entry in spec_reader.paths_and_methods():
                result = differ.check(eio.read(entry),
                                      client.snapshot(entry, method))
                # pprint(list(diff(etalon_d, snap_d, ignore={'headers.Date'})))
                print('{0}:'.format(entry))
                print(result)

    @staticmethod
    def command(args, project: ResortProject):
        """See options.read_args.
        --store -> ResortEngine.store
        --check -> ResortEngine.check

        Args:
            args ([argparse.Namespace]): args is a result of parse_args
            project (ResortProject): read or created project structure
        """
        args.command(project)
