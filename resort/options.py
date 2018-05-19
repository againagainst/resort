'''
Available options:
config - path to the config json file (cli argument only)
project - path to the project directory
server.url - address of a test server
server.schema - definition of a test server
'''
import argparse
import pathlib
import json


def make_argparser():
    parser = argparse.ArgumentParser(description='Provide --project to store an etalon')
    parser.add_argument('-o', '--project',
                        default=argparse.SUPPRESS,
                        type=pathlib.Path,
                        help='path to the project file',
                        dest='project')
    parser.add_argument('-c', '--config',
                        default="config.json",
                        type=pathlib.Path,
                        help='path to the config file, default is "./config.json"',
                        dest='config')
    cmd_group = parser.add_mutually_exclusive_group()
    cmd_group.add_argument("--store", action="store_true")
    cmd_group.add_argument("--check", action="store_true")
    return parser


def command_line_arguments():
    parser = make_argparser()
    args = vars(parser.parse_args())

    store = args.pop('store', None)
    check = args.pop('check', None)
    if store and check:
        raise RuntimeError("The --store can not be used with --check")
    elif store:
        args['mode'] = 'store'
    else:  # Assume --check if no options provided
        args['mode'] = 'check'


def read_config(cfg_file: pathlib.Path):
    with cfg_file.open(mode='r') as cfgf:
        return json.load(cfgf)


def read_all(cfg_file_path='config.json'):
    args = command_line_arguments()
    cfg_file = args.get('config', cfg_file_path)
    cfg = read_config(cfg_file)
    return {**cfg, **args}
