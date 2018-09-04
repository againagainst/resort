import os
import pathlib

import click
import daiquiri

from . import constants
from .project import ResortProject
from .engine import ResortEngine
from .cli import ResortOptions, log_exceptions

@click.group()
@click.option('-v', '--verbose', count=True,
              help='Give more output. Option is additive (up to 2 times).')
@click.option('-q', '--quiet', count=True,
              help='Give less output. Option is additive (up to 3 times).')
@click.pass_context
def cli(ctx, **kwargs):
    """A command-line tool for non-regression testing of RESTful APIs.

    Helps you get better REST!
    """
    ctx.obj = ResortOptions(**kwargs)
    daiquiri.setup(program_name=constants.APP_NAME, level=ctx.obj.loglevel)


@cli.command()
@click.argument('project_dir', type=click.Path(exists=False))
@log_exceptions
def create(project_dir: str):
    """Create boilerplate for new resort project.
    """
    project_path = pathlib.Path(project_dir)
    ResortProject.create(project_path, make_config=True)


@cli.command()
@click.option('-f', '--force',
              is_flag=True, default=False,
              help='Update existing etalons.')
@click.argument('project_dir',
                type=click.Path(exists=True, file_okay=False, writable=True),
                required=False)
def store(project_dir, force):
    """Fetch and store responses as etalons.
    """
    launch(ResortEngine.store, project_dir, update_existing=force)


@cli.command()
@click.argument('project_dir',
                type=click.Path(exists=True, file_okay=False),
                required=False)
def check(project_dir):
    """Compare actual responses to the etalons.
    """
    launch(ResortEngine.check, project_dir, cli=True)


@log_exceptions
def launch(resort_command, project_dir: str=None, *args, **kwargs):
    project_path = pathlib.Path(project_dir or os.getcwd())
    project = ResortProject.read(project_path)
    resort_command(project, *args, **kwargs)


if __name__ == '__main__':
    cli()
