import argparse
import pathlib
import json

parser = argparse.ArgumentParser(description='Provide --output to store an etalon')
parser.add_argument('--output', dest='output', type=pathlib.Path,
                    help='path to the output file')
parser.add_argument('--input', dest='input', type=str,
                    help='path to the input file')
parser.add_argument('--config', dest='config', type=pathlib.Path,
                    help='path to the config file, default is "./config.json"')


def command_line_arguments():
    return vars(parser.parse_args())


def read_config(cfg_file: pathlib.Path):
    with cfg_file.open(mode='r') as cfgf:
        return json.load(cfgf)


def read_all(cfg_file_path='config.json'):
    args = command_line_arguments()
    cfg_file = args.get('config', cfg_file_path)
    cfg = read_config(cfg_file)
    return {**cfg, **args}
