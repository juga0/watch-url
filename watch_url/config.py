"""Configuration for watch-url agent."""
# urljoin only join with one argument
# from urlparse import urljoin
from os.path import join, abspath, dirname
from os import environ

# PATHS
############################
BASE_PATH = abspath(__file__)
# BASE_PATH = abspath('.')
ROOT_PATH = dirname(BASE_PATH)
PROJECT_PATH = dirname(ROOT_PATH)
ROOT_PROJECT_PATH = dirname(PROJECT_PATH)
# in case agents-common-code is not installed, the path to it is requered
AGENTS_MODULE_DIR = 'agents-common-code'
AGENTS_MODULE_PATH = join(ROOT_PROJECT_PATH, AGENTS_MODULE_DIR)

# FIXME: get this name as the name of the module
AGENT_TYPE = 'watch'
AGENT_NAME = 'page-tos'
AGENT_SUFFIX = 'juga'
NAME_SEPARATOR = '-'
SERVICE_NAME = 'watch_page_tos'
# this will be overwroten by the config interval in the store
INTERVAL = 10
# KEY = ['policies', 'urls']
KEY = 'config'

# URLs
############################
# couchdb configuration and urls
STORE_URL = 'https://staging-store.openintegrity.org'
STORE_CONFIG_DB = environ.get('STORE_CONFIG_DB') or 'config'
STORE_CONFIG_DOC = environ.get('STORE_CONFIG_DOC') or \
                    NAME_SEPARATOR.join([AGENT_NAME, AGENT_SUFFIX])
STORE_CONFIG_URL = '/'.join([STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC])
# STORE_CONFIG_URL = https://staging-store.openintegrity.org/config/page-tos-juga

STORE_DB = environ.get('STORE_CONFIG_DOC') or \
    NAME_SEPARATOR.join([AGENT_NAME, AGENT_SUFFIX])
STORE_DB_URL = '/'.join([STORE_URL, STORE_DB])

STORE_LATEST_VIEW = "_design/" + STORE_DB +\
    """/_view/latest?reduce=true&group_level=2&""" \
    """startkey=["%s"]&endkey=["%s",{}]"""
STORE_LATEST_VIEW_URL = '/'.join([STORE_DB_URL, STORE_LATEST_VIEW])
# STORE_LATEST_VIEW_URL = """https://staging-store.openintegrity.org/github-repo-issues/_design/github-repo-issues/_view/latest?reduce=true&group_level=2&startkey=["%s"]&endkey=["%s",{}]"""

STORE_UPDATE_DOC = "_design/" + STORE_DB + "/_update/timestamped/%s"
STORE_UPDATE_DOC_URL = '/'.join([STORE_DB_URL, STORE_UPDATE_DOC])
# STORE_UPDATE_DOC_URL = "https://staging-store.openintegrity.org/github-repo-issues/_design/github-repo-issues/_update/timestamped/analyse-github-repo-issues-84.251.91.165-https-guardianproject.info-home-data-usage-and-protection-policies--etag"


# fetch_github_repo_issues configuration
# FIXME: temporal url for development
# this will be overwritten by the config in the store
FETCH_PAGE_HOST = environ.get('FETCH_PAGE_HOST')
FETCH_PAGE_PORT = environ.get('FETCH_PAGE_PORT')
if FETCH_PAGE_HOST and FETCH_PAGE_PORT:
    FETCH_PAGE_DOMAIN = ":".join(["http://", FETCH_PAGE_HOST, FETCH_PAGE_PORT])
else:
    FETCH_PAGE_DOMAIN = 'http://127.0.0.1:8001'
FETCH_PAGE_NAME = 'fetch_page_tos'
FETCH_PAGE_URL = '/'.join([FETCH_PAGE_DOMAIN, FETCH_PAGE_NAME])

AGENT_PAYLOAD = """{
    "key": "%(key)",
    "agent_ip": "%(agent_ip)",
    "agent_type": "%(agent_type)",
    "header": {
        "etag": "%(etag)",
        "last-modified": "%(last_modified)"
    },
    "content": "%(content)"
}"""


# rabbitmq configuration
AMQP_CONFIG = {'AMQP_URI': 'amqp://guest:guest@localhost'}

# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "%(levelname)s:%(name)s - %(module)s - %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    # 'loggers': {
    #     'nameko': {
    #         'level': 'INFO',
    #         'handlers': ['console']
    #     }
    # },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}
