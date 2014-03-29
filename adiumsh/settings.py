import os
from .utils import get_config


CONFIG_PATH = os.path.expanduser('~/.adiumsh')
PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))
default_config = get_config(CONFIG_PATH, 'default')
DEFAULT_ACCOUNT = \
    default_config.get('account', None) if default_config else None
DEFAULT_SERVICE = \
    default_config.get('service', None) if default_config else None
