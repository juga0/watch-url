"""watch_url."""
# from nameko.rpc import rpc, RpcProxy
from nameko.timer import timer
import sys
import logging
import logging.config
from config import INTERVAL, URLS_KEY, AGENT_TYPE, \
    URLS_CONFIG_URL, URLS_LATEST_URL, URLS_DOC_URL, \
    FETCH_URL_URL, URLS_DATA
from watch_url_util import get_store_rules, get_store_etag, put_store_etag, \
    fetch_url, generate_doc_id, generate_urls_data, url_path_id
try:
    from agents_common.etag_requests import get_etag
    from agents_common.data_structures_utils import get_value_from_key_index
except:
    from config import AGENTS_MODULE_PATH
    sys.path.append(AGENTS_MODULE_PATH)
    from agents_common.etag_requests import get_etag
    from agents_common.data_structures_utils import get_value_from_key_index


logging.basicConfig(level=logging.DEBUG)
try:
    from config import LOGGING
    logging.config.dictConfig(LOGGING)
except:
    print 'No LOGGING configuration found.'
logger = logging.getLogger(__name__)

class WatchURLService(object):
    name ="watchurl"

    # TODO: handle errors
    # TODO: use nameko events
    @timer(interval=INTERVAL)
    def get_config(self):
        data = get_store_rules(URLS_CONFIG_URL)
        # TODO: get these keys and overwrite INTERVAL
        # interval = get_value_from_key_index(data, 'period')
        # trigger:
        rules = get_value_from_key_index(data, URLS_KEY)
        if rules:
            self.watch_url(rules)
        else:
            logger.info('No urls found.')
            sys.exit()

    def watch_url(self, rules):
        # TODO: handle errors
        for rule in rules:
        # FIXME: for development only using 1 rule
            # rule = rules[0]
            url = rule['url']
            # get db etag
            etag_store, last_modified_store = get_store_etag(URLS_LATEST_URL %
                                                             (url, url))
            # get page etag
            etag, last_modified = get_etag(url)
            # compare etags
            # if there weren't any etag in the database, it will be different
            # to the one retrieved from the page and therefore it will also be
            # stored in the database and the content fetched
            if (etag_store != etag) or (last_modified_store != last_modified):
                logger.info('The page has been modified.')
                url_path = url_path_id(etag, last_modified)
                doc_id = generate_doc_id(AGENT_TYPE, url, url_path)
                # store etag in store
                etag_doc_url = URLS_DOC_URL % (doc_id)
                urls_data_dict = generate_urls_data(AGENT_TYPE, url,
                                                    etag, last_modified)
                # TODO: manage conflict when status code 409
                put_store_etag(etag_doc_url, urls_data_dict)
                logger.debug(urls_data_dict)
                # TODO: overwrite FETCH_URL_URL
                r = fetch_url(FETCH_URL_URL, urls_data_dict)
                if r == 503:
                    sys.exit()
            else:
                logger.info('The page has not been modified.')
            # FIXME: for developing exits here
            sys.exit()

# TODO: add main
