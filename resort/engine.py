import daiquiri

from .etalons import EtalonIO, BaseComparator
from .client import BasicClient
from .server_spec import ServerSpecReader
from .project import ResortProject
from .errors import EtalonDirIsNotEmpty

LOG = daiquiri.getLogger(__name__)


class ResortEngine:

    @staticmethod
    def store(project: ResortProject, update_existing=False):
        if not update_existing and project.has_etalons():
            raise EtalonDirIsNotEmpty()

        for each_test in project.test_specs:
            LOG.info('Storing: ' + str(each_test))
            client = BasicClient(ServerSpecReader.prepare(spec_file=each_test))
            eio = EtalonIO(project=project, make_dir=True)
            for etalon in client.snapshot_etalons():
                eio.save(etalon)

    @staticmethod
    def check(project: ResortProject, cli=True):
        check_hash = dict(changes=0)
        for each_test in project.test_specs:
            LOG.info('Cheking: ' + str(each_test))
            client = BasicClient(ServerSpecReader.prepare(spec_file=each_test))
            differ = BaseComparator(ignored=project.ignored)
            eio = EtalonIO(project=project)
            for snapshot in client.snapshot_etalons():
                etalon = eio.restore(snapshot)
                result = differ.check(etalon, snapshot)
                check_hash['changes'] += result['changes']
                assert etalon.entry == snapshot.entry
                check_hash[(etalon.file_name, etalon.entry)] = result
                if cli:
                    print('{0} | {1}:'.format(etalon.file_name, etalon.entry))
                    print(result['difftext'])
        return check_hash
