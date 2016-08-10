"""watch_url functions."""
import sys
import requests
import logging
from requests.exceptions import ConnectionError
try:
    from agents_common.scraper_utils import url2filenamedashes, \
        last_modified2timestamp_str, now_timestamp_ISO_8601
    from agents_common.system_utils import obtain_public_ip
    from agents_common.data_structures_utils import get_value_from_key_index
except ImportError as e:
    print('agents_common is not installed '
          'or does not contain one of the required modules,'
          ' trying to find it inside this program path')
    try:
        from config import AGENTS_MODULE_PATH
        sys.path.append(AGENTS_MODULE_PATH)
        from agents_common.scraper_utils import url2filenamedashes, \
            last_modified2timestamp_str, now_timestamp_ISO_8601
        from agents_common.system_utils import obtain_public_ip
        from agents_common.data_structures_utils import get_value_from_key_index
    except ImportError as e:
        print('agents_common not found in this program path, '
              'you need to install it or'
              ' create a symlink inside this program path')
        sys.exit()

from config_common import AGENT_PAYLOAD, AGENT_ATTRIBUTE

logger = logging.getLogger(__name__)
# print 'LOG LEVEL watch_url_utils...'
# print logging.getLevelName(logger.getEffectiveLevel())


def url_path_id(etag=None, last_modified=None):
    # timestamp is not the the system timestamp but the etag/last_modified
    if etag:
        tag = etag
    elif last_modified:
        tag = last_modified2timestamp_str(last_modified)
    else:
        tag = ''
    return tag


def generate_doc_id(agent_type, url, url_path_id=''):
    """
    Return and string like:
    analyse-url-192.168.1.1-https-www.whispersystems.org-signal-privacy-20160613T190136Z.
    """
    ip = obtain_public_ip()
    urlfilename = url2filenamedashes(url)
    doc_id = '-'.join([agent_type, ip, urlfilename, url_path_id])
    logger.debug('doc_id %s', doc_id)
    return doc_id


def generate_urls_data(url, agent_type, page_type, etag='', last_modified='',
                       xpath='', content='', attribute=AGENT_ATTRIBUTE, ):
    """
    https://staging-store.openintegrity.org/pages-juga/_design/page/_update/timestamped/watch-176.10.104.243-httpsguardianproject.infohomedata-usage-and-protection-policies-
    data = {'agent_ip': '78.142.19.213',
     'agent_type': 'watch',
     'page_type': 'tos',
     'content': '',
     'header': {'etag': '', 'last_modified': ''},
     'key': u'https://guardianproject.info/home/data-usage-and-protection-policies/',
     'timestamp_measurement': '2016-07-29T23:13:15.511Z',
     'xpath': '//article'}

    new schema:

     {
         "entity": "%(entity)",
         "attribute": "page/content",
         "value": {
             "header": {
                 "etag": "%(etag)",
                 "last-modified": "%(last_modified)"
             },
             "content": "%(content)",
             "sha256_html": "%(sha256_html)",
             "sha256_md": "%(sha256_md)"
         },
         "context": {
             "timestamp_measurement": "%(timestamp_measurement)",
             "agent_type": "%(agent_type)",
             "agent_ip": "%(agent_ip)",
             "page_type": "%(page_type)",
             "xpath": "%(xpath)"
         }
     }
    """
    # data = {
    #     'entity': url,
    #     'attribute': attribute,
    #     'value': {
    #         'header': {
    #             'etag': etag,
    #             'last_modified': last_modified
    #             }
    #         },
    #     "context": {
    #         'agent_ip':  obtain_public_ip(),
    #         'agent_type': agent_type,
    #         'page_type': page_type,
    #         'timestamp_measurement': now_timestamp_ISO_8601(),
    #         'xpath': xpath
    #         }
    #     }
    data = AGENT_PAYLOAD % {
        'entity': url,
        'attribute': attribute,
        'etag': etag,
        'last_modified': last_modified,
        'agent_ip':  obtain_public_ip(),
        'agent_type': agent_type,
        'page_type': page_type,
        'timestamp_measurement': now_timestamp_ISO_8601(),
        'xpath': xpath
    }
    return data


def get_store(url, json_key=None):
    logger.debug('GET url %s', url)
    r = requests.get(url)
    logger.info('Reguest GET %s returns %s', url, r.reason)
    logger.debug('Response: %s', r)
    try:
        logger.debug('Response content is json.')
        data = r.json()
    except ValueError:
        logger.debug('Response content is not json')
        return r.text
    if json_key:
        logger.debug('Searching for json key %s in the response.', json_key)
        value = get_value_from_key_index(data, json_key)
        logger.debug('The value of the key is %s', value)
        return value
    return data


def put_store(url, data, only_status_code=False):
    logger.debug('PUT url %s' % url)
    # TODO: create database if it doesn't exist
    if isinstance(data, dict):
        r = requests.put(url, json=data)
    else:
        r = requests.put(url, data=data)
    logger.info('Reguest PUT %s returns %s', url, r.reason)
    if only_status_code:
        return r.status_code
    return r


def post_store(url, data, only_status_code=False):
    logger.info('POST url %s' % url)
    if isinstance(data, dict):
        try:
            r = requests.post(url, json=data)
        except ConnectionError as e:
            logger.error(e)
            return None
    else:
        try:
            r = requests.post(url, data=data)
        except ConnectionError as e:
            logger.error(e)
            return None
    logger.info('Request POST %s returned %s', url, r.reason)
    if only_status_code:
        return r.status_code
    return r


def get_store_rules(url, rules_key='config'):
    """
    """
    return get_store(url)


def get_store_etag(url):
    # TODO: manage conflict when status code 409
    etag = last_modified = ''
    rows = get_store(url, 'rows')
    if rows:
        keys_indexes = [0, 'value', 'header', 'etag']
        try:
            etag = get_value_from_key_index(rows, keys_indexes)
        except KeyError, IndexError:
            logger.debug('etag not found either the document was not stored '
                         'or the query is wrong.')
            keys_indexes = [0, 'value', 'header', 'last_modified']
            try:
                last_modified = get_value_from_key_index(rows, keys_indexes)
            except KeyError, IndexError:
                logger.debug('last_modified not found either the document was '
                             'not stored or the query is wrong.')
                pass
    else:
        logger.error('No content in rows, something must be wrong.')
    return etag, last_modified

def put_store_etag(url, data):
    """
    Put in the store the etag or last_modified for a given url.
    The url of the store is like this:
    watch-url-89.31.96.168-https-guardianproject.info-home-data-usage-and-\
    protection-policies--\
    20160613T190136Z
    The json data structure is like this:
    {
    "key":"https://www.whispersystems.org/signal/privacy/",
    "agent_ip": "1.2.3.4",
    "agent_type":"watch-url",
    "timestamp_measurements": "20160623T120243Z",
    "header":{
        "etag":"",
        "last-modified":"Mon, 13 Jun 2016 19:01:36 GMT"
        },
    "content":""
    }
    """
    # To create new document you can either use a POST operation or a PUT operation. To create/update a named document using the PUT operation
    # To update an existing document, you also issue a PUT request. In this case, the JSON body must contain a _rev property, which lets CouchDB know which revision the edits are based on. If the revision of the document currently stored in the database doesn't match, then a 409 conflict error is returned.
    # It is recommended that you avoid POST when possible, because proxies and other network intermediaries will occasionally resend POST requests, which can result in duplicate document creation. If your client software is not capable of guaranteeing uniqueness of generated UUIDs, use a GET to /_uuids?count=100 to retrieve a list of document IDs for future PUT requests. Please note that the /_uuids-call does not check for existing document ids; collision-detection happens when you are trying to save a document.
    # FIXME: manage conflict
    return put_store(url, data, only_status_code=True)


def post_store_etag(url, data):
    """
    Like put_store_etag but using method POST
    """
    logger.info('post_store_etag being called')
    return post_store(url, data, only_status_code=True)


def fetch_url(url, data):
    """
    {'content': '',
    'agent_ip': '109.163.234.2',
    'agent_type': u'https://guardianproject.info/home/data-usage-and-protection-policies/',
    'key': 'watch-url',
    'header': {
        'etag': None,
        'last_modified': None
        }
    }
    """
    return post_store(url, data, only_status_code=True)
