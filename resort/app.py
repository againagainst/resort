import json

import options
import etalons
from client import BasicClient
from server_spec import ServerSpecReader


class ResortApp:

    @staticmethod
    def launch():
        """TODO: Add description docstring
        """
        opts = options.command_line_arguments()
        launcher = opts['mode'].select(store=ResortApp.store,
                                       check=ResortApp.check,
                                       create=ResortApp.create)
        if not opts['mode'].is_create():
            opts = options.read_all()
        launcher(opts)

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
        project_dir.mkdir(parents=False, exist_ok=False)
        project_name = project_dir.stem
        config_file = project_dir.joinpath(options.CONFIG_FILE_NAME)
        apispec_file = project_dir.joinpath(options.APISPEC_FILE_NAME)
        with apispec_file.open('w') as sfp:
            json.dump(ResortApp._spec_content(project_name=project_name),
                      sfp,
                      indent=2)
        with config_file.open('w') as cfp:
            json.dump(ResortApp.__default_config, cfp, indent=2)

    @staticmethod
    def _spec_content(*, project_name):
        spec = ResortApp.__default_spec
        spec['info']['title'] = project_name
        return spec

    __default_config = {
        "server": {
            "spec": options.APISPEC_FILE_NAME,
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


if __name__ == '__main__':
    ResortApp.launch()
