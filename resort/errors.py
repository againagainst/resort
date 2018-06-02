
class ResortBaseException(Exception):
    """Base class for all Resort framework exceptions."""
    pass


class BadArgument(ResortBaseException):
    """Raised when unsupported CL argument provided.

    Args:
        reason (str): what is invalid (and why)
    """

    def __init__(self, reason):
        super().__init__("Invalid argument: %s" % reason)


class BadProjectPath(BadArgument):
    """Raised when Resort is unable to write to the project directory.

    Args:
        path (pathlib.Path): invalid path
    """
    def __init__(self, path):
        super().__init__("project_dir - can not create files in %s" % path)


class BadConfiguration(ResortBaseException):
    """Raised when a config property is missing or invalid.

    Args:
        reason (str): what is invalid (and why)
    """

    def __init__(self, reason):
        super().__init__("Invalid configuration: %s" % reason)
