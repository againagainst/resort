import json

import daiquiri

import constants
import etalons
from errors import BadProjectPath, BadArgument
from client import BasicClient
from server_spec import ServerSpecReader

LOG = daiquiri.getLogger(__name__)


class ResortEngine:

    @staticmethod
    def store(opts: dict):
        """TODO: Add description docstring

        Args:
            opts (dict): [description]
        """
        client = BasicClient(server_url=opts['server']['url'],
                             spec_file=opts['server']['spec']
                             ).prepare()
        eio = etalons.EtalonIO(project_dir=opts['project'], make_dir=True)
        for etalon in client.snapshot_etalons():
            eio.save(etalon)

    @staticmethod
    def check(opts: dict):
        """TODO: Add description docstring

        Args:
            opts (dict): [description]
        """
        spec_reader = ServerSpecReader(opts['server']['spec']).prepare()
        client = BasicClient(server_url=opts['server']['url'])
        differ = etalons.BaseComparator(ignored={'headers.Date'})
        eio = etalons.EtalonIO(project_dir=opts['project'])
        for method, entry in spec_reader.paths_and_methods():
            result = differ.check(eio.read(entry), client.snapshot(entry, method))
            # pprint(list(diff(etalon_d, snap_d, ignore={'headers.Date'})))
            print('{0}:'.format(entry))
            print(result)

    @staticmethod
    def create(opts: dict):
        """Creates a project directory:
        resort/app.py --create --project=/path/to/project_dir

        Result:
        project_dir/
            config.json
            apispec.json

        Args:
            opts (dict):
        """
        project_dir = opts['project']
        # TODO: make a ResortProject class, move this functionality
        try:
            project_dir.mkdir(parents=False, exist_ok=False)
        except FileNotFoundError as exc:
            raise BadProjectPath(path=exc.filename)
        except FileExistsError as exc:
            raise BadArgument('project_dir - directory "%s" '
                              'already exists.' % exc.filename)
        project_name = project_dir.stem
        config_file = project_dir.joinpath(constants.CONFIG_FILE_NAME)
        apispec_file = project_dir.joinpath(constants.APISPEC_FILE_NAME)
        with apispec_file.open('w') as sfp:
            LOG.info('Creating {0}'.format(apispec_file))
            json.dump(ResortEngine._spec_content(project_name=project_name),
                      sfp,
                      indent=2)
        with config_file.open('w') as cfp:
            LOG.info('Creating {0}'.format(config_file))
            json.dump(ResortEngine.__default_config, cfp, indent=2)

    @staticmethod
    def _spec_content(*, project_name):
        spec = ResortEngine.__default_spec
        spec['info']['title'] = project_name
        return spec

    __default_config = {
        "server": {
            "spec": constants.APISPEC_FILE_NAME,
            "url": "http://127.0.0.1"
        }
    }
    __default_spec = {
        "info": {
            "version": "1.0.0",
            "description": ""
        },
        "paths": {
            "/index.html": {
                "get": {}
            }
        },
        "tags": [],
        "definitions": {},
        "parameters": {}
    }
