APP_NAME = 'Resort'
APP_DESCRIPTION = 'Resort - Test automation tool for the RESTful APIs.'


CONFIG_FILE_NAME = 'config.json'


class ResortMode:
    """Mode of the application, at the moment can be `store`, `check` or `create`"""
    STORE = 'store'
    CHECK = 'check'
    CREATE = 'create'
    ANY = {STORE, CHECK, CREATE}