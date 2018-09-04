import logging
import functools

import daiquiri

from .errors import ResortBaseException

LOG = daiquiri.getLogger(__name__)


class ResortOptions(object):

    def __init__(self, **kwargs):
        self.loglevel = ResortOptions.get_log_level(**kwargs)
        self.config = kwargs.get('config')

    @staticmethod
    def get_log_level(**kwargs):
        """
        NOTHING  > 50: -qqq
        CRITICAL = 50: -qq
        ERROR    = 40: -q --quiet
        WARNING  = 30: default
        INFO     = 20: -v --verbose
        DEBUG    = 10: -vv
        """
        verbose = kwargs.get('verbose')
        quiet = kwargs.get('quiet')

        if quiet == verbose:
            return logging.WARNING
        elif quiet > 0:
            return logging.WARNING + min(quiet, 3) * 10
        else:
            return logging.WARNING - min(verbose, 2) * 10


def log_exceptions(command):
    """Logs all resort exceptions as warnings.
    """
    @functools.wraps(command)
    def wrapper(*args, **kwargs):
        try:
            return command(*args, **kwargs)
        except ResortBaseException as exc:
            LOG.warning(exc)
    return wrapper
