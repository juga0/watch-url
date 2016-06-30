"""Configuration for watch-url agent."""
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

# FIXME: get this name as the name of the module
AGENT_TYPE = 'watch-url'
# this will be overwroten by the config interval in the store
INTERVAL = 10
# URLS_KEY = ['policies', 'urls']
URLS_KEY = 'config'

# couchdb configuration and urls
STORE_URL = 'https://staging-store.openintegrity.org'
URLS_CONFIG_DB = 'config'
URLS_CONFIG_DOC = 'tos'
URLS_CONFIG_URL = '/'.join([STORE_URL, URLS_CONFIG_DB, URLS_CONFIG_DOC])
# URLS_CONFIG_URL = https://staging-store.openintegrity.org/config/tos

URLS_DB = 'url'
URLS_LATESTS_VIEW = """_design/url/_view/latest?reduce=true&group_level=2&startkey=["%s"]&endkey=["%s",{}]"""
URLS_LATEST_URL = '/'.join([STORE_URL, URLS_DB, URLS_LATESTS_VIEW])
# URLS_LATEST_URL = """https://staging-store.openintegrity.org/url/_design/url/_view/latest?reduce=true&group_level=2&startkey=["%s"]&endkey=["%s",{}]"""

URLS_DB_URL = '/'.join([STORE_URL, URLS_DB])
URLS_DOC_URL = '/'.join([URLS_DB_URL, "%s"])
# URLS_DOC_URL = "https://staging-store.openintegrity.org/url/analyse-url-84.251.91.165-https-guardianproject.info-home-data-usage-and-protection-policies--etag"
URLS_DATA = """{
    "key": "%(key)",
    "agent_ip": "%(agent_ip)",
    "agent_type": "%(agent_type)",
    "header": {
        "etag": "%(etag)",
        "last-modified": "%(last_modified)"
    },
    "content": "%(content)"
}"""



# fetch_url configuration
# FIXME: temporal url for development
# this will be overwroten by the config in the store
FETCH_URL_DOMAIN = 'http://127.0.0.1:8001'
FETCH_URL_NAME = 'fetchurl'
FETCH_URL_URL = '/'.join([FETCH_URL_DOMAIN, FETCH_URL_NAME])

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
