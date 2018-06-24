import logging

import daiquiri

import constants
import options
from project import ResortProject
from errors import ResortBaseException

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
            args = options.read_args()
            if args.mode.lower() == constants.ResortMode.CREATE:
                ResortProject.create(args.project)
            else:
                project = ResortProject.read(args.project)
                opts = options.read_all()
                args.command(project, opts)
        except ResortBaseException as exc:
            LOG.warning(exc)


if __name__ == '__main__':
    ResortApp.launch()
