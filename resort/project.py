import json
import pathlib

import daiquiri

from . import constants, options
from .errors import BadProjectPath, BadArgument

LOG = daiquiri.getLogger(__name__)


class ResortProject(object):
    """Represents a project of the Resort tool.

    Args:
        name (str, optional): Defaults to stem of the project_dir
        config (dict, optional): Defaults to None.
        test_specs (tuple): list of test_specs files (aka test_* files)
    """

    def __init__(self, project_dir: pathlib.Path,
                 name: str=None, test_specs: tuple=None, config: dict=None):
        # pkey, id
        self.project_dir = project_dir
        # optional
        self.name = name or project_dir.stem
        self.test_specs = test_specs or tuple()
        self.config = config or ResortProject.__default_config
        self.ignored = {'headers.Date'}

    @classmethod
    def create(cls, project_dir: pathlib.Path, make_config: bool=False):
        """Creates a project directory:
        resort/app.py --project=/path/to/project_dir create

        Result:
            project_dir/
                test_first.json - a test stub
                config.json - optional, various project cofigurations

        Args:
            project_dir (pathlib.Path): [full path to project]
            make_config (bool, optional): Defaults to False. [generates the config.json
            stub if True]

        Raises:
            BadProjectPath: [description]
            BadArgument: [description]

        Returns:
            [ResortProject]: [A project instance]
        """
        try:
            project_dir.mkdir(parents=False, exist_ok=False)
        except FileNotFoundError as exc:
            raise BadProjectPath(path=exc.filename)
        except FileExistsError as exc:
            raise BadArgument('project_dir - directory "%s" already exists.' % exc.filename)

        test_file = project_dir.joinpath(ResortProject.__default_testfile_name)
        with test_file.open('w') as sfp:
            LOG.info('Creating {0}'.format(test_file))
            json.dump(ResortProject.__default_testfile, sfp, indent=2)

        if make_config:
            config_file = project_dir.joinpath(constants.CONFIG_FILE_NAME)
            with config_file.open('w') as cfp:
                LOG.info('Creating {0}'.format(config_file))
                json.dump(ResortProject.__default_config, cfp, indent=2)
        return cls(project_dir)

    @classmethod
    def read(cls, project_dir: pathlib.Path, opts: dict):
        """Reads projects configuration (config) and reolves test files (specs).

        Args:
            project_dir (pathlib.Path): path to the project

        Returns:
            ResortProject: instance of the class
        """
        default_config = project_dir.joinpath(options.CONFIG_FILE_NAME)
        return cls(project_dir,
                   test_specs=options.resolve_test_files(project_dir=project_dir),
                   config=options.read_config(default_config))

    def resolve_project_dir(self, make_dir=False):
        """Checks if project dir can be created:
        - self.project_dir is not an existing file

            make_dir (bool, optional): Defaults to False. Creates directory,
            does nothing if the directory exists.

        Raises:
            BadProjectPath: if self.project_dir is invalid

        Returns:
            pathlib.Path: self.project_dir
        """
        if self.project_dir.exists() and not self.project_dir.is_dir():
            raise BadProjectPath(self.project_dir)
        if make_dir:
            self.project_dir.mkdir(parents=True, exist_ok=True)
        return self.project_dir

    __default_config = {
        'exclude': []
    }

    __default_testfile_name = 'test_unknown.json'

    __default_testfile = {
        "info": {
            "description": "generated test stub",
            "version": "1.0.0"
        },
        "server": {
            "url": "http://127.0.0.1:8888"
        },
        "paths": [
            ["/index.html", "get"]
        ]
    }
