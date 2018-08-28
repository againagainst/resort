import logging
import pathlib
import functools

import click
import daiquiri

from resort import constants
from resort.project import ResortProject
from resort.engine import ResortEngine
from resort.errors import ResortBaseException

# setup logging
daiquiri.setup(program_name=constants.APP_NAME,
               level=logging.DEBUG if __debug__ else logging.INFO)
LOG = daiquiri.getLogger(constants.APP_NAME)


def log_exceptions(command):
    @functools.wraps
    def wrapper(*args, **kwargs):
        try:
            return command(*args, **kwargs)
        except ResortBaseException as exc:
            LOG.warning(exc)
    return wrapper


@click.group()
def cli():
    pass


@cli.command()
def create(project_dir: str):
    project_path = pathlib.Path(project_dir)
    ResortProject.create(project_path, make_config=True)


@cli.command()
def store(project_dir: str=None):
    launch(ResortEngine.store, project_dir)


@cli.command()
def check(project_dir: str=None):
    launch(ResortEngine.check, project_dir, cli=True)


def launch(command, project_dir: str, *args, **kwargs):
    project_path = pathlib.Path(project_dir)
    project = ResortProject.read(project_path)
    command(project, *args, **kwargs)
