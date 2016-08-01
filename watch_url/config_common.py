"""Common configuration for watch/fetch/analyse-page-tos agents."""
# urljoin only join with one argument
# from urlparse import urljoin
from os.path import join, abspath, dirname
from os import environ

DEBUG = environ.get('DEBUG') or False
DATA_DIR_DEFAULT = 'data'
LOG_FILE_DEFAULT = 'log/info.log'
CONSOLE_LOG_DEFAULT = 'ERROR'
AGENTS_MODULE_DIR = 'agents-common-code'
STORE_URL_DEFAULT = 'https://staging-store.openintegrity.org'

PAGE_TYPE = 'tos'
AGENT_NAME = 'pages'
AGENT_SUFFIX = 'juga'
NAME_SEPARATOR = '-'
# this will be overwritten by the config interval in the store
INTERVAL = 60
CONFIG_DOC_KEY = 'config'

# paths
############################
BASE_PATH = abspath(__file__)
ROOT_PATH = dirname(BASE_PATH)
PROJECT_PATH = dirname(ROOT_PATH)
ROOT_PROJECT_PATH = dirname(PROJECT_PATH)
# in case agents-common-code is not installed, the path to it is requered
AGENTS_MODULE_PATH = join(ROOT_PROJECT_PATH, AGENTS_MODULE_DIR)

# fs store
FS_PATH = environ.get('FS_PATH') or join(PROJECT_PATH, DATA_DIR_DEFAULT)

# URLs
############################
# couchdb configuration and urls
STORE_URL = environ.get('STORE_URL') or STORE_URL_DEFAULT
STORE_CONFIG_DB = environ.get('STORE_CONFIG_DB') or 'config'
STORE_CONFIG_DOC = environ.get('STORE_CONFIG_DOC') or \
                    NAME_SEPARATOR.join([AGENT_NAME, AGENT_SUFFIX])
STORE_CONFIG_URL = '/'.join([STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC])
# STORE_CONFIG_URL = https://staging-store.openintegrity.org/config/page-tos-juga

# data
############################
AGENT_PAYLOAD = """{
    "key": "%(key)",
    "agent_ip": "%(agent_ip)",
    "agent_type": "%(agent_type)",
    "page_type": "%(page_type)",
    "header": {
        "etag": "%(etag)",
        "last-modified": "%(last_modified)"
    },
    "content": "%(content)"
    "timestamp_measurement": "%(timestamp_measurement)"
}"""

# logging
LOG_PATH = environ.get('LOG_PATH') or join(PROJECT_PATH, LOG_FILE_DEFAULT)
LOG_LEVEL = environ.get('LOG_LEVEL') or \
            ('DEBUG' if DEBUG else CONSOLE_LOG_DEFAULT)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': "%(levelname)s:%(module)s - %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': LOG_LEVEL
        },
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": LOG_PATH,
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": LOG_PATH,
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    'loggers': {
        'nameko': {
            'level': 'DEBUG',
            'handlers': ['console', 'info_file_handler']
        },
        # uncomment this to get logs only from these modules and comment root
        # FIXME: see FIXME in root
        'watch_url': {
            # DEBUG must be here to catch all possible logs that will get filtered
            # by the handler
            'level': 'DEBUG',
            'handlers': ['console', 'debug_file_handler']
        },
        'watch_url_util': {
            'level': 'DEBUG',
            'handlers': ['console', 'debug_file_handler']
        }
    },
    'root': {
        # # DEBUG must be here to catch all possible logs that will get filtered
        # # by the handler
        # # FIXME: watch_url* don't log here where this uncommented
        # # and watch_url* commented
        # 'level': 'DEBUG',
        # 'handlers': ['console', 'debug_file_handler']
    }
}

# nameko
############################
CONFIG_YAML_PATH = join(ROOT_PATH, 'config.yaml')
WEB_SERVER_ADDRESS = '127.0.0.1:8000'
# rabbitmq configuration
# this doesn't have any effect here
# AMQP_CONFIG = {'AMQP_URI': 'amqp://guest:guest@localhost'}
