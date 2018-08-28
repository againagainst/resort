import logging

import daiquiri

from resort import constants, options
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
            args = options.read_args()
            if args.mode.lower() == constants.ResortMode.CREATE:
                ResortProject.create(args.project, make_config=True)
            else:
                project = ResortProject.read(args.project)
                ResortApp.invoke_engine(args, project)
        except ResortBaseException as exc:
            LOG.warning(exc)

    @staticmethod
    def invoke_engine(args, project: ResortProject):
        """See options.read_args.
        `store` -> ResortEngine.store
        `check` -> ResortEngine.check

        Args:
            args ([argparse.Namespace]): args is a result of parse_args
            project (ResortProject): read or created project structure
        """
        args.command(project)


if __name__ == '__main__':
    ResortApp.launch()
