"""Common functions for OII Agents."""
# urljoin only join with one argument
# from urlparse import urljoin
from os.path import join, abspath, dirname


BASE_PATH = abspath(__file__)
# BASE_PATH = abspath('.')
ROOT_PATH = dirname(BASE_PATH)
PROJECT_PATH = dirname(ROOT_PATH)
ROOT_PROJECT_PATH = dirname(PROJECT_PATH)
# in case agents-common-code is not installed, the path to it is requered
AGENTS_MODULE_DIR = 'agents-common-code'
AGENTS_MODULE_PATH = join(ROOT_PROJECT_PATH, AGENTS_MODULE_DIR)

# FIXME: the ide should be generated other way
AGENT_ID = 'agent-tos-1'

# configuration yaml file. All the configuration here could go there
CONFIG = join(ROOT_PATH, 'config.yaml')

# interval of time in which the agent is going to retrieve its configuration
INTERVAL = 10

# couchdb configuration and urls
COUCHDB_URL = 'https://oii-db.iilab.org'
TOS_CONFIG_DB = 'staging-config'
TOS_CONFIG_DOC = 'tos'
# TOS_CONFIG_URL = 'https://oii-db.iilab.org/staging-config/tos'
TOS_CONFIG_URL = '/'.join([COUCHDB_URL, TOS_CONFIG_DB, TOS_CONFIG_DOC])
TOS_ETAG_URL = """https://oii-db.iilab.org/staging-tos/_design/couchapp-tos/_view/tos?reduce=true&group_level=2&startkey=["%s"]&endkey=["%s",{}]"""
# TOS_ETAG_POST_URL = "https://oii-db.iilab.org/staging-tos/tos-1"

TOS_ETAG_DB = 'staging-tos'
# FIXME: should be this a hash of the agent and the url?
# TOS_ETAG_DOC = 'tos-1'
# TOS_ETAG_POST_URL = '/'.join([COUCHDB_URL, TOS_ETAG_DB, TOS_ETAG_DOC])
TOS_ETAG_DOC = AGENT_ID + '-%s'
TOS_ETAG_PART_POST_URL = '/'.join([COUCHDB_URL, TOS_ETAG_DB]) + '/%s'

# fetch_url configuration
# FIXME: temporal url for development
FETCH_URL = 'http://127.0.0.1:8000/fetchurl/%s/%s/%s'

# rabbitmq configuration
AMQP_CONFIG = {'AMQP_URI': 'amqp://guest:guest@localhost'}

# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': "%(levelname)s:%(name)s - %(module)s - %(message)s"
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'nameko': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}
