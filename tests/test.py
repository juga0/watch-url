""" Unit testing...
"""
# run with  py.test -s tests/test.py
import logging
from nameko.testing.services import worker_factory

try:
    from agents_common.etag_requests import get_etag
    from agents_common.data_structures_utils import get_value_from_key_index
except ImportError:
    from watch_url.config import AGENTS_MODULE_PATH
    sys.path.append(AGENTS_MODULE_PATH)
    from agents_common.etag_requests import get_etag
    from agents_common.data_structures_utils import get_value_from_key_index

from watch_url.config_common import INTERVAL, KEY, AGENT_PAYLOAD
from watch_url.config import AGENT_TYPE, STORE_CONFIG_URL, STORE_LATEST_VIEW_URL, \
    STORE_UPDATE_DOC_URL, FETCH_PAGE_URL

from watch_url.watch_url_util import get_store_rules, get_store_etag, post_store_etag, \
    fetch_url, generate_doc_id, generate_urls_data, url_path_id

logging.basicConfig(level=logging.DEBUG)
try:
    from watch_url.config_common import LOGGING
    logging.config.dictConfig(LOGGING)
except:
    print 'No LOGGING configuration found.'
logger = logging.getLogger(__name__)


# def test_get_config():
#     return_value = {
#         u'policy': u'privacy_policy',
#         u'organization': u'theguardianproject',
#         u'tool': u'chatsecure',
#         u'url': u'https://guardianproject.info/home/data-usage-and-protection-policies/',
#         u'xpath': u'//article'
#     }
#     data = get_store_rules(STORE_CONFIG_URL)
#     assert data['config'][0] == return_value


# def test_gen_store_update_url_payload():
#     url = u'https://guardianproject.info/home/data-usage-and-protection-policies/'
#     etag = None
#     last_modified = None
#     xpath = u'//article'
#     url_store_update = 'https://staging-store.openintegrity.org/pages-juga/_design/pages-juga/_update/timestamped/watch-176.10.104.243-httpsguardianproject.infohomedata-usage-and-protection-policies-'
#     payload = "{'xpath': u'//article', 'agent_ip': '78.142.19.213', 'content': '', 'header': {'etag': None, 'last_modified': None}, 'agent_type': 'watch', 'key': u'https://guardianproject.info/home/data-usage-and-protection-policies/', 'timestamp_measurements': '20160729T231315Z'}{'xpath': u'//article', 'agent_ip': '78.142.19.213', 'content': '', 'header': {'etag': None, 'last_modified': None}, 'agent_type': 'watch', 'key': u'https://guardianproject.info/home/data-usage-and-protection-policies/', 'timestamp_measurements': '20160729T231315Z'}"
#     url_path = url_path_id(etag, last_modified)
#     doc_id = generate_doc_id(AGENT_TYPE, url, url_path)
#     # store etag in store
#     etag_doc_url = STORE_UPDATE_DOC_URL % (doc_id)
#     logger.debug('The URL to store the page is %s', etag_doc_url)
#     urls_data_dict = generate_urls_data(AGENT_TYPE, url,
#                                         etag, last_modified,
#                                         xpath=xpath)
#     logger.debug('The data to store the page is %s', urls_data_dict)
#     assert etag_doc_url == url_store_update
#     assert urls_data_dict == payload


def test_post_update_pages():
    url_store_update = 'https://staging-store.openintegrity.org/pages-juga/_design/pages-juga/_update/timestamped/watch-176.10.104.243-httpsguardianproject.infohomedata-usage-and-protection-policies-'
    payload = "{'xpath': u'//article', 'agent_ip': '78.142.19.213', 'content': '', 'header': {'etag': None, 'last_modified': None}, 'agent_type': 'watch', 'key': u'https://guardianproject.info/home/data-usage-and-protection-policies/', 'timestamp_measurements': '20160729T231315Z'}{'xpath': u'//article', 'agent_ip': '78.142.19.213', 'content': '', 'header': {'etag': None, 'last_modified': None}, 'agent_type': 'watch', 'key': u'https://guardianproject.info/home/data-usage-and-protection-policies/', 'timestamp_measurements': '20160729T231315Z'}"
    return_value = 'OK'
    assert return_value == post_store_etag(url_store_update, payload)
