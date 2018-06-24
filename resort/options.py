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
from errors import BadConfiguration
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
    subparsers.add_parser(ResortMode.CREATE,
                          help='Creates a project directory, --project is required')
    store_parser = subparsers.add_parser(ResortMode.STORE,
                                         help='TODO: store help')
    store_parser.set_defaults(command=ResortEngine.store)
    check_parser = subparsers.add_parser(ResortMode.CHECK,
                                         help='TODO:  check help')
    check_parser.set_defaults(command=ResortEngine.check)
    return parser.parse_args()


def read_config(cfg_file: pathlib.Path):
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


def resolve_test_files(project_dir: pathlib.Path=None, filetype='json'):
    """Finds all test_* files in the project directory.

    Args:
        project_dir: pathlib.Path:  full path to the project
    Returns:
        list: of pathlib.Paths to each test_* files
    """
    if project_dir is None:
        args = vars(read_args())
        project_dir = args['project']

    return list(project_dir.glob('test_*.{filetype}'.format(filetype=filetype)))


def read_all():
    """Convenient way to get all the options specified by user.
    Note, that CLI args has higher priority than config options.

    Returns:
      dict: cli args + config options + list of test files
    """
    args = vars(read_args())
    # resolve config
    project_dir = args['project']
    default_config = project_dir.joinpath(CONFIG_FILE_NAME)
    cfg_file = args.get('config', default_config)
    cfg = read_config(cfg_file) if cfg_file else dict()
    tests = resolve_test_files(project_dir=project_dir)
    return {**cfg, **args, "tests": tests}
