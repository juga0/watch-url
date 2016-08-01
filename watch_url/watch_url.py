"""watch_url."""
import sys
import logging
import logging.config

from nameko.timer import timer

try:
    from agents_common.etag_requests import get_etag
    from agents_common.data_structures_utils import get_value_from_key_index
except ImportError:
    print('agents_common is not installed '
          'or does not contain one of the required modules,'
          ' trying to find it inside this program path')
    try:
        from config import AGENTS_MODULE_PATH
        sys.path.append(AGENTS_MODULE_PATH)
        from agents_common.etag_requests import get_etag
        from agents_common.data_structures_utils import \
            get_value_from_key_index
    except ImportError:
        print('agents_common not found in this program path, '
              'you need to install it or'
              ' create a symlink inside this program path')
        sys.exit()
from config_common import INTERVAL, CONFIG_DOC_KEY, AGENT_PAYLOAD, PAGE_TYPE
from config import AGENT_TYPE, STORE_CONFIG_URL, STORE_LATEST_VIEW_URL, \
    STORE_UPDATE_DOC_URL, FETCH_PAGE_URL

from watch_url_util import get_store_rules, get_store_etag, post_store_etag, \
    fetch_url, generate_doc_id, generate_urls_data, url_path_id

try:
    from config_common import LOGGING
    logging.config.dictConfig(LOGGING)
except ImportError:
    print "Couldn't find LOGGING in config.py"
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class WatchURLService(object):
    name = SERICE_NAME

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
            # sys.exit()
        else:
            logger.info('No urls found.')
            sys.exit()
        # sys.exit()

    def watch_url(self, rules):
        # TODO: handle errors
        # FIXME: for development only using 1 rule
        # logger.debug("rule 0 %s", rules[0])
        # for rule in [rules[0]]:
        for rule in rules:
            logger.debug('Processing rule with url %s', rule['url'])
            url = rule['url']
            # get db etag
            etag_store, last_modified_store = \
                get_store_etag(STORE_LATEST_VIEW_URL % (url, url))
            logger.debug('Etag value in store is %s and last_modified is %s',
                         etag_store, last_modified_store)
            # get page etag
            etag, last_modified = get_etag(url)
            logger.debug('Etag value in page is %s and last_modified is %s',
                         etag, last_modified)
            # compare etags
            # if there weren't any etag in the database, it will be different
            # to the one retrieved from the page and therefore it will also be
            # stored in the database and the content fetched
            # when the page doesn't have etag nor last_modified, it's stored
            if (etag_store == etag == '' and
                last_modified_store == last_modified == '') or\
                (etag_store != etag) or\
                (last_modified_store != last_modified):

                logger.info('The page has been modified or it have not'
                            'etag nor last_modified information.')
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
                logger.info('POST store returned %s', r)
                # call fetch
                logger.info('Requesting fetch on %s.', FETCH_PAGE_URL)
                logger.debug('data %s', urls_data_dict)
                r = fetch_url(FETCH_PAGE_URL, urls_data_dict)
                if r is None or r == 503:
                    logger.info('There was a problem trying to connect to'
                                ' the fetch agent, is it running?.')
                    sys.exit()
                logger.info('Sent request to fetch')
            else:
                logger.info('The page has not been modified.')
            # FIXME: for developing exits after 1st rule
            # sys.exit()

# TODO: add main
