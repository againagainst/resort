'''
Available options:
config - path to the config json file (cli argument only)
project - path to the project directory
server.url - address of a test server
server.spec - definition of a test server
'''
import argparse
import os
import pathlib
import json

from engine import ResortEngine
from errors import BadArgument, BadConfiguration
from constants import APP_DESCRIPTION, CONFIG_FILE_NAME, ResortMode


def read_args():
    """Setups the argparse.ArgumentParser to parse all
    available options for the application

    Returns:
        ArgumentParser: parser
    """
    parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
    parser.add_argument('-p', '--project',
                        default=pathlib.Path(os.getcwd()),
                        type=pathlib.Path,
                        help='path to the project directory',
                        dest='project')
    subparsers = parser.add_subparsers(help='TODO: commands help',
                                       dest='mode')
    create_parser = subparsers.add_parser(ResortMode.CREATE,
                                          help='TODO: create help')
    create_parser.set_defaults(command=ResortEngine.create)
    store_parser = subparsers.add_parser(ResortMode.STORE,
                                         help='TODO: store help')
    store_parser.set_defaults(command=ResortEngine.store)
    check_parser = subparsers.add_parser(ResortMode.CHECK,
                                         help='TODO:  check help')
    check_parser.set_defaults(command=ResortEngine.check)
    return parser.parse_args()


def read_config(cfg_file: pathlib.Path):
    """
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
        raise BadArgument('--config - No such file: "%s"' % cfg_file)


def read_all():
    """Convenient way to get all the options specified by user.
    Note, that CLI args has higher priority than config options.

    Args:
      cfg_file_path: str (Default value = 'config.json'):
      full path to the configuration file
    Returns:
      dict: cli args + config options
    """
    args = vars(read_args())
    # resolve config
    project_dir = args['project']
    default_config = project_dir.joinpath(CONFIG_FILE_NAME)
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
