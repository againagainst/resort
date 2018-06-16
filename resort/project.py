import json
import pathlib

import daiquiri

import constants
from errors import BadProjectPath, BadArgument

LOG = daiquiri.getLogger(__name__)


class ResortProject(object):
    """TODO: class description

    Args:
        name ([type]): [description]
        config (dict, optional): Defaults to None. [description]
    """

    def __init__(self, name, config: dict=None):
        self.name = name
        self.config = config or ResortProject.__default_config

    @classmethod
    def create(cls, project_dir: pathlib.Path, make_config: bool=False):
        """TODO: method description

        Args:
            project_dir (pathlib.Path): [description]
            make_config (bool, optional): Defaults to False. [description]

        Raises:
            BadProjectPath: [description]
            BadArgument: [description]

        Returns:
            [type]: [description]
        """
        try:
            project_dir.mkdir(parents=False, exist_ok=False)
        except FileNotFoundError as exc:
            raise BadProjectPath(path=exc.filename)
        except FileExistsError as exc:
            raise BadArgument('project_dir - directory "%s" already exists.' % exc.filename)

        project_name = project_dir.stem
        test_file = project_dir.joinpath(ResortProject.__default_testfile_name)
        with test_file.open('w') as sfp:
            LOG.info('Creating {0}'.format(test_file))
            json.dump(ResortProject.__default_testfile, sfp, indent=2)

        if make_config:
            config_file = project_dir.joinpath(constants.CONFIG_FILE_NAME)
            with config_file.open('w') as cfp:
                LOG.info('Creating {0}'.format(config_file))
                json.dump(ResortProject.__default_config, cfp, indent=2)
        return cls(project_name)

    @classmethod
    def read(cls, project_dir: pathlib.Path):
        """TODO: method description

        Args:
            project_dir (pathlib.Path): [description]

        Returns:
            [type]: [description]
        """
        project_name = project_dir.stem
        # TODO: read config
        # TODO: make list of test files
        return cls(project_name)

    __default_config = {
        'exclude': []
    }

    __default_testfile_name = 'test_unknown.json'

    __default_testfile = {
        "info": {
            "title": "unknown",
            "description": "generated test stub",
            "version": "1.0.0"
        },
        "server": {
            "url": "http://127.0.0.1"
        },
        "paths": [
            ["/index.html", "get"]
        ]
    }
