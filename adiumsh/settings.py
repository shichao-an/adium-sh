import os
from .utils import get_config


PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))
REPO_PATH = os.path.join(PACKAGE_PATH, os.pardir)
LOG_PATH = '~/Library/Application Support/Adium 2.0/Users/Default/Logs'
LOG_PATH = os.path.expanduser(LOG_PATH)
CONFIG_PATH = os.path.expanduser('~/.adiumsh') \
    if not os.environ.get('ADIUMSH_TEST') \
    else os.path.join(REPO_PATH, '.adiumsh')

default_config = get_config(CONFIG_PATH, 'default')
DEFAULT_ACCOUNT = \
    default_config.get('account', None) if default_config else None
DEFAULT_SERVICE = \
    default_config.get('service', None) if default_config else None
DEFAULT_BUDDY = \
    default_config.get('buddy', None) if default_config else None
