import os
import json
import pathlib

import daiquiri

from . import constants
from .errors import BadArgument, BadConfiguration, BadProjectPath

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
        self._etalons_dir = project_dir.joinpath(pathlib.Path('etalons'))
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
    def read(cls, project_dir: pathlib.Path):
        """Reads projects configuration (config) and reolves test files (specs).

        Args:
            project_dir (pathlib.Path): path to the project

        Returns:
            ResortProject: instance of the class
        """
        default_config = project_dir.joinpath(constants.CONFIG_FILE_NAME)
        return cls(project_dir,
                   test_specs=cls.resolve_test_files(project_dir=project_dir),
                   config=cls.read_config(default_config))

    @classmethod
    def read_config(cls, cfg_file: pathlib.Path):
        """Reads the given config file

        Args:
        cfg_file: pathlib.Path:
        full path to the configuration file

        Returns:
        dict: config.json loaded
        """
        try:
            with cfg_file.open(mode='r') as cfgf:
                return json.load(cfgf)
        except FileNotFoundError:
            raise BadConfiguration('No such file: "%s"' % cfg_file)

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

    @classmethod
    def resolve_test_files(cls, project_dir: pathlib.Path, filetype='json'):
        """Finds all test_* files in the project directory.

        Args:
            project_dir: pathlib.Path:  full path to the project
        Returns:
            list: of pathlib.Paths to each test_* files
        """
        return list(project_dir.glob('test_*.{filetype}'.format(filetype=filetype)))

    def has_etalons(self):
        return self.etalons_dir.exists() and len(os.listdir(str(self.etalons_dir))) > 0

    @property
    def etalons_dir(self):
        """
        Returns:
            [pathlib.Path]: directory for etalons, relative to the project_dir
        """
        return self._etalons_dir

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
        "requests": [
            ["/index.html", "get"]
        ]
    }
