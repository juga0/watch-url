"""watch_url."""
import sys
import logging
import logging.config

from nameko.timer import timer

try:
    from agents_common.etag_requests import get_etag
    from agents_common.data_structures_utils import get_value_from_key_index
except ImportError:
    from config import AGENTS_MODULE_PATH
    sys.path.append(AGENTS_MODULE_PATH)
    from agents_common.etag_requests import get_etag
    from agents_common.data_structures_utils import get_value_from_key_index

from config_common import INTERVAL, CONFIG_DOC_KEY, AGENT_PAYLOAD
from config import AGENT_TYPE, STORE_CONFIG_URL, STORE_LATEST_VIEW_URL, \
    STORE_UPDATE_DOC_URL, FETCH_PAGE_URL

from watch_url_util import get_store_rules, get_store_etag, post_store_etag, \
    fetch_url, generate_doc_id, generate_urls_data, url_path_id


logging.basicConfig(level=logging.DEBUG)
try:
    from config_common import LOGGING
    logging.config.dictConfig(LOGGING)
except ImportError:
    print "Couldn't find LOGGING in config.py"
logger = logging.getLogger(__name__)
print("logger name %s" % logger.name)

class WatchURLService(object):
    name = "watchurl"

    # TODO: handle errors
    # TODO: use nameko events
    @timer(interval=INTERVAL)
    def get_config(self):
        data = get_store_rules(STORE_CONFIG_URL)
        # TODO: get these keys and overwrite INTERVAL
        # interval = get_value_from_key_index(data, 'period')
        # trigger:
        rules = get_value_from_key_index(data, CONFIG_DOC_KEY)
        if rules:
            logger.info('Found %s rules.', len(rules))
            self.watch_url(rules)
            # for debugging, exit after first rule
            sys.exit()
        else:
            logger.info('No urls found.')
            sys.exit()
        sys.exit()

    def watch_url(self, rules):
        # TODO: handle errors
        # for rule in rules:
        # FIXME: for development only using 1 rule
        logger.debug("rule 0 %s", rules[0])
        for rule in [rules[0]]:
            logger.debug('Processing rule with url %s', rule['url'])
            url = rule['url']
            # get db etag
            etag_store, last_modified_store = \
                get_store_etag(STORE_LATEST_VIEW_URL % (url, url))
            logger.debug('Found etag %s and last_modified %s in store',
                         etag_store, last_modified_store)
            # get page etag
            etag, last_modified = get_etag(url)
            logger.debug('Found etag %s and last_modified %s in web site',
                         etag, last_modified)
            # compare etags
            # if there weren't any etag in the database, it will be different
            # to the one retrieved from the page and therefore it will also be
            # stored in the database and the content fetched
            # when the page doesn't have etag nor last_modified, it's stored
            if (etag_store == etag == '' and
                        last_modified_store == last_modified == '') or
                    (etag_store != etag) or
                    (last_modified_store != last_modified):
                logger.info('The page has been modified.')
                url_path = url_path_id(etag, last_modified)
                doc_id = generate_doc_id(AGENT_TYPE, url, url_path)
                # store etag in store
                etag_doc_url = STORE_UPDATE_DOC_URL % (doc_id)
                logger.debug('The URL to store the page is %s', etag_doc_url)
                urls_data_dict = generate_urls_data(url,
                                                    AGENT_TYPE, PAGE_TYPE,
                                                    etag, last_modified,
                                                    xpath=rule['xpath'])
                # logger.debug(urls_data_dict)
                # TODO: manage conflict when status code 409
                logger.info('Saving etag/last_modified in store.')
                r = post_store_etag(etag_doc_url, urls_data_dict)
                logger.info('POST store returned %s', r.reason)
                # logger.debug('Requesting fetch.')
                # r = fetch_url(FETCH_PAGE_URL, urls_data_dict)
                # if r is None or r == 503:
                #     logger.error('There was a problem trying to connect to'
                #                  ' the fetch agent.')
                #     sys.exit()
                # logger.info('Contacting fetch')
            else:
                logger.info('The page has not been modified.')
            # FIXME: for developing exits here
            sys.exit()

# TODO: add main
