"""watch_url."""
# from nameko.rpc import rpc, RpcProxy
from nameko.timer import timer
from nameko.runners import ServiceRunner
from nameko.testing.utils import get_container
import yaml
import logging
import logging.config
# from logger import LoggingDependency
from config import CONFIG, AMQP_CONFIG, INTERVAL, \
    TOS_CONFIG_URL, TOS_ETAG_URL, TOS_ETAG_DOC, TOS_ETAG_PART_POST_URL,\
    FETCH_URL
from couchdb_watch import get_db_rules, get_db_etag, put_db_etag, fetch_url
try:
    from agents_common.etag_requests import get_etag
except:
    from config import AGENTS_MODULE_PATH
    import sys
    sys.path.append(AGENTS_MODULE_PATH)
    from agents_common.etag_requests import get_etag


logging.basicConfig(level=logging.DEBUG)
with open(CONFIG) as fle:
    config = yaml.load(fle)
if "LOGGING" in config:
    logging.config.dictConfig(config['LOGGING'])
logger = logging.getLogger(__name__)

class WatchURLService(object):
    name ="watchurl"
    # logger = LoggingDependency()

    @timer(interval=INTERVAL)
    def get_config(self):
        rules = get_db_rules(TOS_CONFIG_URL)
        logger.debug(rules)
        self.watch_url(rules)

    def watch_url(self, rules):
        # for rule in rules:
        # for development only using 1 rule
            rule = rules[0]
            url = rule['url']
            # get db etag
            # logger.debug('requesting etag in db for url %s', url)
            # get db etag
            etag_db, last_modified_db = get_db_etag(TOS_ETAG_URL % (url, url))
            # get page etag
            etag, last_modified = get_etag(url)
            # compare etags
            # if there weren't any etag in the database, it will be different
            # to the one retrieved from the page and therefore it will also be
            # stored in the database and the content fetched
            if (etag_db != etag) or (last_modified_db != last_modified):
                logger.info('the page has been modified')
                # store etag in db
                tos_etag_doc = TOS_ETAG_DOC % (rule['organization'] + '-' + rule['tool'] + '-' + rule['policy'])
                tos_etag_post_url = TOS_ETAG_PART_POST_URL % tos_etag_doc
                # TODO: manage conflict when status code 409
                put_db_etag(tos_etag_post_url, url, etag, last_modified)
                fetch_url(FETCH_URL % (url, etag, last_modified))
            logger.info('the page has not been modified')

def main():
    logging.basicConfig(level=logging.DEBUG)
    # with open(CONFIG) as fle:
    #     config = yaml.load(fle)
    # if "LOGGING" in config:
    #     logging.config.dictConfig(config['LOGGING'])
    # # logger = logging.getLogger('nameko')
    # # logger = logging.getLogger(__name__)
    # logging.debug('before start')
    with open(CONFIG) as fle:
        config = yaml.load(fle)
    if "LOGGING" in config:
        logging.config.dictConfig(config['LOGGING'])
    logger = logging.getLogger(__name__)
    logger.debug('before start')

    runner = ServiceRunner(AMQP_CONFIG)
    runner.add_service(WatchURLService)
    # runner.add_service(ServiceB)
    # ``get_container`` will return the container for a particular service
    container_watchurl = get_container(runner, WatchURLService)
    # start both services
    runner.start()
    logging.debug('stop')
    # stop both services
    # runner.stop()


if __name__ == '__main__':
    main()
