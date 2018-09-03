import os
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
    @functools.wraps(command)
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
@click.argument('project_dir', type=click.Path(exists=False))
@log_exceptions
def create(project_dir: str):
    project_path = pathlib.Path(project_dir)
    ResortProject.create(project_path, make_config=True)


@cli.command()
@click.option('--project',
              type=click.Path(exists=True, file_okay=False, writable=True),
              default=None)
def store(project: str=None):
    launch(ResortEngine.store, project)


@cli.command()
@click.option('--project',
              type=click.Path(exists=True, file_okay=False, writable=True),
              default=None)
def check(project: str=None):
    launch(ResortEngine.check, project, cli=True)


@log_exceptions
def launch(command, project_dir: str=None, *args, **kwargs):
    project_path = pathlib.Path(project_dir or os.getcwd())
    project = ResortProject.read(project_path)
    command(project, *args, **kwargs)
