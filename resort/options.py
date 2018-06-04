'''
Available options:
config - path to the config json file (cli argument only)
project - path to the project directory
server.url - address of a test server
server.spec - definition of a test server
'''
import argparse
import pathlib
import json

from errors import BadArgument, BadConfiguration
from constants import CONFIG_FILE_NAME


class ResortMode:
    """Mode of the application

    Args:
        name (str): mode name, can be
        `store`, `check` or `create`

    Raises:
        RuntimeError: if the given mode name is unknown
    """
    STORE = 'store'
    CHECK = 'check'
    CREATE = 'create'
    ANY = {STORE, CHECK, CREATE}

    def __init__(self, name: str):
        if name not in ResortMode.ANY:
            raise BadArgument("Mode %s is not supported" % name)
        self.name = name

    def is_store(self) -> bool:
        return self.name == ResortMode.STORE

    def is_check(self) -> bool:
        return self.name == ResortMode.CHECK

    def is_create(self) -> bool:
        return self.name == ResortMode.CREATE

    def select(self, **kwargs):
        return kwargs[self.name]

    def __repr__(self):
        return 'ResortMode({!r})'.format(self.name)


def make_argparser():
    """Setups the argparse.ArgumentParser to parse all
    available options for the application

    Returns:
        ArgumentParser: parser
    """

    parser = argparse.ArgumentParser(
        description='Resort - Test automation tool for the RESTful APIs.')
    cmd_group = parser.add_mutually_exclusive_group(required=True)
    cmd_group.add_argument("--store",
                           action="store_const",
                           const=ResortMode("store"),
                           dest='mode')
    cmd_group.add_argument("--check",
                           action="store_const",
                           const=ResortMode("check"),
                           dest='mode')
    cmd_group.add_argument("--create",
                           action="store_const",
                           const=ResortMode("create"),
                           dest='mode')
    parser.add_argument('-o', '--project',
                        default=argparse.SUPPRESS,
                        type=pathlib.Path,
                        help='path to the project file',
                        dest='project')
    parser.add_argument('-c', '--config',
                        default=argparse.SUPPRESS,
                        type=pathlib.Path,
                        help='path to the config file, default is "./config.json"',
                        dest='config')
    return parser


def command_line_arguments():
    """
    Raises:
        RuntimeError: when user tries to `store` and
        `check` at the same time
    Returns:
        dict: arguments
    """
    parser = make_argparser()
    return vars(parser.parse_args())


def read_config(cfg_file: pathlib.Path):
    """
    Args:
      cfg_file: pathlib.Path:
      full path to the configuration file
    Returns:
      dict: config.json loaded
    """
    with cfg_file.open(mode='r') as cfgf:
        return json.load(cfgf)


def read_all():
    """Convenient way to get all the options specified by user.
    Note, that CLI args has higher priority than config options.

    Args:
      cfg_file_path: str (Default value = 'config.json'):
      full path to the configuration file
    Returns:
      dict: cli args + config options
    """
    args = command_line_arguments()
    project_dir = args['project']
    # resolve config
    default_config = project_dir.joinpath(CONFIG_FILE_NAME) if project_dir else None
    cfg_file = args.get('config', default_config)
    cfg = read_config(cfg_file) if cfg_file else dict()

    # resolve spec
    try:
        spec_path = pathlib.Path(cfg['server']['spec'])
        if not spec_path.is_absolute():
            spec_path = project_dir.joinpath(spec_path)
            cfg['server']['spec'] = spec_path
    except KeyError:
        raise BadConfiguration("Server API Specification is not defined. "
                               "Add server.spec section to the %s" % cfg_file)
    return {**cfg, **args}
