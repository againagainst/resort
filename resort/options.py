'''
Available options:
config - path to the config json file (cli argument only)
output - path to the output directory
server.url - address of a test server
server.schema - definition of a test server
'''
import argparse
import pathlib
import json


def make_argparser():
    parser = argparse.ArgumentParser(description='Provide --output to store an etalon')
    parser.add_argument('-o', '--output',
                        default=argparse.SUPPRESS,
                        type=pathlib.Path,
                        help='path to the output file',
                        dest='output')
    parser.add_argument('-c', '--config',
                        default="config.json",
                        type=pathlib.Path,
                        help='path to the config file, default is "./config.json"',
                        dest='config')
    return parser


def command_line_arguments():
    parser = make_argparser()
    return vars(parser.parse_args())


def read_config(cfg_file: pathlib.Path):
    with cfg_file.open(mode='r') as cfgf:
        return json.load(cfgf)


def read_all(cfg_file_path='config.json'):
    args = command_line_arguments()
    cfg_file = args.get('config', cfg_file_path)
    cfg = read_config(cfg_file)
    return {**cfg, **args}
