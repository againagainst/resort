from resort.test import sysinfo # noqa

import logging

import daiquiri

from resort import constants
from resort.options import read_args, read_all
from resort.engine import ResortEngine
from resort.project import ResortProject
from resort.errors import ResortBaseException

# setup logging
daiquiri.setup(program_name=constants.APP_NAME,
               level=logging.DEBUG if __debug__ else logging.INFO)
LOG = daiquiri.getLogger(constants.APP_NAME)


class ResortApp:

    @staticmethod
    def launch():
        """Main function of the application.
        Reads cli argumnets, calls engine's command, loggs errors.
        """
        try:
            args = read_args()
            if args.mode.lower() == constants.ResortMode.CREATE:
                ResortProject.create(args.project, make_config=True)
            else:
                project = ResortProject.read(
                    args.project, opts=read_all())
                ResortEngine.command(args, project)
        except ResortBaseException as exc:
            LOG.warning(exc)


if __name__ == '__main__':
    ResortApp.launch()
