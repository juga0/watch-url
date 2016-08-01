#!/usr/bin/env python
"""watch_url."""
import logging
import yaml

from os import environ

from nameko.runners import ServiceRunner
from nameko.testing.utils import get_container

from watch_url import WatchURLService

# try:
#     from config_common import LOGGING, CONFIG_YAML_PATH, WEB_SERVER_ADDRESS
#     logging.config.dictConfig(LOGGING)
# except ImportError:
#     print 'No LOGGING configuration found.'
#     logging.basicConfig(level=logging.DEBUG)
from config_common import LOGGING, CONFIG_YAML_PATH, WEB_SERVER_ADDRESS
logging.config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)

def update_config_yaml(config_dict, path):
    WATCH_PAGE_HOST = environ.get('WATCH_PAGE_HOST')
    WATCH_PAGE_PORT = environ.get('WATCH_PAGE_PORT')
    if WATCH_PAGE_HOST and WATCH_PAGE_PORT:
        WEB_SERVER_ADDRESS = ":".join(["http://",
                                       WATCH_PAGE_HOST, WATCH_PAGE_PORT])
        config_dict['WEB_SERVER_ADDRESS'] = WEB_SERVER_ADDRESS
    elif config_dict.get('WEB_SERVER_ADDRESS') is None:
        config_dict['WEB_SERVER_ADDRESS'] = WEB_SERVER_ADDRESS
    with open(path, 'w') as f:
        s = yaml.dump(config_dict)
        f.write(s)
    return config_dict


def get_config_yaml(path):
    with open(path) as f:
        y = f.read()
        c = yaml.load(y)
    return c


def main():
    config_dict = get_config_yaml(CONFIG_YAML_PATH)
    c = update_config_yaml(config_dict, CONFIG_YAML_PATH)
    runner = ServiceRunner(c)
    runner.add_service(WatchURLService)
    # container_a = get_container(runner, WatchURLService)
    runner.start()
    try:
        runner.wait()
    except KeyboardInterrupt:
        runner.kill()
    runner.stop()
    # sys.exit()

if __name__ == '__main__':
    main()
