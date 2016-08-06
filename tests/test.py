""" Unit testing...
"""
# run with  py.test -s tests/test.py
import json
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

from watch_url.config_common import INTERVAL, CONFIG_DOC_KEY, AGENT_PAYLOAD, PAGE_TYPE, AGENT_ATTRIBUTE
from watch_url.config import AGENT_TYPE, STORE_CONFIG_URL, STORE_LATEST_VIEW_URL, \
    STORE_UPDATE_DOC_URL, FETCH_PAGE_URL

from watch_url.watch_url_util import get_store_rules, get_store_etag, post_store_etag, \
    fetch_url, generate_doc_id, generate_urls_data, url_path_id

logger = logging.getLogger(__name__)


def test_get_config():
    return_value = {
        u'policy': u'privacy_policy',
        u'organization': u'theguardianproject',
        u'tool': u'chatsecure',
        u'url': u'https://guardianproject.info/home/data-usage-and-protection-policies/',
        u'xpath': u'//article'
    }
    data = get_store_rules(STORE_CONFIG_URL)
    assert data['config'][0] == return_value


def test_gen_store_update_url_payload():
    url = 'https://guardianproject.info/home/data-usage-and-protection-policies/'
    etag = ''
    last_modified = ''
    xpath = '//article'
    doc_id = 'watch-176.10.104.243-httpsguardianproject.infohomedata-usage-and-protection-policies-'
    url_store_update = STORE_UPDATE_DOC_URL % (doc_id)
    payload = {
        "entity": "https://guardianproject.info/home/data-usage-and-protection-policies/",
        "attribute": "page/content",
        "value": {
            "header": {
                "etag": "",
                "last_modified": ""
            }
        },
        "context": {
            "xpath": "//article",
            # "agent_ip": "78.142.19.213",
            "agent_type": "watch",
            "page_type": "tos",
            # "timestamp_measurement": "2016-07-29T23:13:15.511Z"
        }
    }
    url_path = url_path_id(etag, last_modified)
    doc_id = generate_doc_id(AGENT_TYPE, url, url_path)
    # store etag in store
    etag_doc_url = STORE_UPDATE_DOC_URL % (doc_id)
    logger.debug('The URL to store the page is %s', etag_doc_url)
    urls_data_dict = generate_urls_data(url,
                                        AGENT_TYPE, PAGE_TYPE,
                                        etag, last_modified,
                                        xpath=xpath,
                                        attribute=AGENT_ATTRIBUTE)
    # logger.debug('The data to store the page is %s', urls_data_dict)
    # ip will be different, remove the ip
    u = '-'.join(url_store_update.split('-')[0:2] +
                 url_store_update.split('-')[4:])
    e = '-'.join(etag_doc_url.split('-')[0:2] +
                 etag_doc_url.split('-')[4:])
    assert u == e
    # payload.pop('agent_ip')
    # payload.pop('timestamp_measurement')
    logging.debug(urls_data_dict)
    urls_data_dict["context"].pop('agent_ip')
    urls_data_dict["context"].pop('timestamp_measurement')
    assert payload == urls_data_dict


def test_post_update_pages():
    url_store_update = 'https://staging-store.openintegrity.org/pages-juga/_design/page/_update/timestamped/watch-176.10.104.243-httpsguardianproject.infohomedata-usage-and-protection-policies-'
    payload = """{"attribute": "page/content", "context": {"timestamp_measurement": "2016-08-04T01:06:18.125782Z", "agent_ip": "185.69.168.112", "agent_type": "watch", "page_type": "tos", "xpath": "//article"}, "value": {"header": {"etag": "", "last_modified": ""}}, "entity": "https://guardianproject.info/home/data-usage-and-protection-policies/"}"""
    return_value = 201
    assert return_value == post_store_etag(url_store_update, payload)


def test_get_latest_pages_view_url():
    url = "https://guardianproject.info/home/data-usage-and-protection-policies/"
    latest_url = 'https://staging-store.openintegrity.org/pages-juga/_design/page/_view/latest?reduce=true&group_level=2&startkey=["https://guardianproject.info/home/data-usage-and-protection-policies/"]&endkey=["https://guardianproject.info/home/data-usage-and-protection-policies/",{}]'
    assert STORE_LATEST_VIEW_URL % (url, url) == latest_url


def test_get_latest_pages_view():
    url = "https://guardianproject.info/home/data-usage-and-protection-policies/"
    etag = last_modified = ''
    etag_store, last_modified_store = \
        get_store_etag(STORE_LATEST_VIEW_URL % (url, url))
    assert etag == etag_store
    assert last_modified == last_modified_store


def test_fetch_url():
    url_fetch = 'http://127.0.0.1:8001/fetch_page_tos'
    assert FETCH_PAGE_URL == url_fetch


def test_post_fetch_url():
    payload = '{"xpath": "//article", "agent_ip": "78.142.19.213", "content": "", "header": {"etag": "", "last_modified": ""}, "agent_type": "watch", "page_type": "tos", "key": "https://guardianproject.info/home/data-usage-and-protection-policies/", "timestamp_measurement": "2016-07-29T23:13:15.511Z"}'
    return_value = 200
    r = fetch_url(FETCH_PAGE_URL, payload)
    assert return_value == r
