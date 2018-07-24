import daiquiri

from resort import etalons
from .client import BasicClient
from .server_spec import ServerSpecReader
from .project import ResortProject

LOG = daiquiri.getLogger(__name__)


class ResortEngine:

    @staticmethod
    def store(project: ResortProject):
        for each_test in project.test_specs:
            LOG.info('Storing: ' + str(each_test))
            client = BasicClient(ServerSpecReader.prepare(spec_file=each_test))
            eio = etalons.EtalonIO(project=project, make_dir=True)
            for etalon in client.snapshot_etalons():
                eio.save(etalon)

    @staticmethod
    def check(project: ResortProject):
        for each_test in project.test_specs:
            LOG.info('Cheking: ' + str(each_test))
            client = BasicClient(ServerSpecReader.prepare(spec_file=each_test))
            differ = etalons.BaseComparator(ignored=project.ignored)
            eio = etalons.EtalonIO(project=project)
            for snapshot in client.snapshot_etalons():
                etalon = eio.restore(snapshot)
                result = differ.check(etalon, snapshot)
                print('{0} | {1}:'.format(etalon.file_name, etalon.entry))
                assert etalon.entry == snapshot.entry
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
