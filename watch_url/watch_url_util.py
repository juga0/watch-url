"""watch_url functions."""
import requests
import logging
try:
    from agents_common.scraper_utils import url2filenamedashes, \
        last_modified2timestamp_str
    from agents_common.system_utils import obtain_public_ip
    from agents_common.data_structures_utils import get_value_from_key_index
except:
    from config import AGENTS_MODULE_PATH
    import sys
    sys.path.append(AGENTS_MODULE_PATH)
    from agents_common.scraper_utils import url2filenamedashes, \
        last_modified2timestamp_str
    from agents_common.system_utils import obtain_public_ip
    from agents_common.data_structures_utils import get_value_from_key_index

logging.basicConfig(level=logging.DEBUG)
try:
    from config import LOGGING
    logging.config.dictConfig(LOGGING)
except:
    print 'No LOGGING configuration found.'
logger = logging.getLogger(__name__)


def generate_agent_id(agent_type, url, etag=None, last_modified=None):
    """
    Return and string like:
    analyse-url-192.168.1.1-https-www.whispersystems.org-signal-privacy-20160613T190136Z.
    """
    ip = obtain_public_ip()
    urlfilename = url2filenamedashes(url)
    # timestamp is not the the system timestamp but the etag/last_modified
    if etag:
        tag = etag
    elif last_modified:
        tag = last_modified2timestamp_str(last_modified)
    else:
        tag = ''
    agent_id = '-'.join([agent_type, ip, urlfilename, tag])
    logger.debug('agent_id %s', agent_id)
    return agent_id


def generate_urls_data(data_urls_str, agent_type, url, etag, last_modified):
    '''
    >>> data_urls_str = """{
    'key': '%(key)',
    'agent_ip': '%(agent_ip)',
    'agent_type': '%(agent_type)',
    'header': {
        'etag': '%(etag)',
        'last-modified': '%(last_modified)'
    },
    'content': '%(content)'
    }"""
    >>> urls_data_dict = {'agent_ip': '85.248.227.164', 'etag': None, 'key': u'https://guardianproject.info/home/data-usage-and-protection-policies/', 'agent_type': 'watch-url', 'last_modified': None, 'content': None}
    >>> urls_data_str_subs = data_urls_str % urls_data_dict
    >>> data_urls_str = """{
    'key': '{key}',
    'agent_ip': '{agent_ip}',
    'agent_type': '{agent_type}',
    'header': {
        'etag': '{etag}',
        'last-modified': '{last_modified}'
    },
    'content': '{content}'
    }"""
    '''
    # urls_data_dict = {
    #     'key': url,
    #     'agent_ip': obtain_public_ip(),
    #     'agent_type': agent_type,
    #     'etag': etag,
    #     'last_modified': last_modified,
    #     # 'content': None
    # }
    # logger.debug('data_urls_str %s', data_urls_str)
    # logger.debug('urls_data_dict %s', urls_data_dict)
    # urls_data_str_subs = data_urls_str % urls_data_dict
    # urls_data_dict_subs = json.loads(urls_data_str_subs)
    urls_data_dict_subs = {
        'key': url,
        'agent_ip':  obtain_public_ip(),
        'agent_type': agent_type,
        'header': {
            'etag': etag,
            'last_modified': last_modified
            },
        'content': ''
        }
    return urls_data_dict_subs


def get_store(url, json_key=None):
    logger.debug('GET url %s', url)
    r = requests.get(url)
    try:
        data = r.json()
    except ValueError:
        return r.text
    if json_key:
        logger.debug('json key %s', json_key)
        value = get_value_from_key_index(data, json_key)
        return value
    return data


def put_store(url, data, only_status_code=False):
    logger.debug('PUT url %s' % url)
    if isinstance(data, dict):
        r = requests.put(url, json=data)
    else:
        r = requests.put(url, data=data)
    if only_status_code:
        return r.status_code
    return r


def post_store(url, data, only_status_code=False):
    logger.debug('POST url %s' % url)
    if isinstance(data, dict):
        r = requests.post(url, json=data)
    else:
        r = requests.post(url, data=data)
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

    # logger.debug('url %s', url)
    # r = requests.get(url)
    # if r.json().get("rows"):
    #     try:
    #         etag = r.json()['rows'][0]['value']['header'].get('etag')
    #         last_modified = r.json()['rows'][0]['value']['header'].get('last-modified')
    #     except KeyError, IndexError:
    #         logger.debug('no key etag or/nor last_modified in db')
    # logger.debug('etag %s', etag)
    # logger.debug('last-modified %s', last_modified)
    # return etag, last_modified

    rows = get_store(url, 'rows')
    if rows:
        keys_indexes = ['rows', 0, 'value', 'header', 'etag']
        try:
            etag = get_value_from_key_index(rows, keys_indexes)
        except KeyError, IndexError:
            keys_indexes = ['rows', 0, 'value', 'header', 'last_modified']
            try:
                last_modified = get_value_from_key_index(rows, keys_indexes)
            except KeyError, IndexError:
                pass
    return etag, last_modified

def put_store_etag(url_store, urls_data_dict):
    """
    Put in the store the etag or last_modified for a given url.
    The url of the store is like this:
    watch-url-89.31.96.168-https-guardianproject.info-home-data-usage-and-\
    protection-policies--\
    308260b059be166829326014df56da5d5b59b3157944f8612cfe51925aacc0ae
    The json data structure is like this:
    {
    "key":"https://www.whispersystems.org/signal/privacy/",
    "agent_ip": "89.31.96.168",
    "agent_type":"watch-url",
    "header":{
        "etag":"",
        "last-modified":"Mon, 13 Jun 2016 19:01:36 GMT"
        },
    "content":"# Privacy Policy\n\n..."
    }
    """
    # To create new document you can either use a POST operation or a PUT operation. To create/update a named document using the PUT operation
    # To update an existing document, you also issue a PUT request. In this case, the JSON body must contain a _rev property, which lets CouchDB know which revision the edits are based on. If the revision of the document currently stored in the database doesn't match, then a 409 conflict error is returned.
    # It is recommended that you avoid POST when possible, because proxies and other network intermediaries will occasionally resend POST requests, which can result in duplicate document creation. If your client software is not capable of guaranteeing uniqueness of generated UUIDs, use a GET to /_uuids?count=100 to retrieve a list of document IDs for future PUT requests. Please note that the /_uuids-call does not check for existing document ids; collision-detection happens when you are trying to save a document.
    # FIXME: manage conflict
    return put_store(url_store, urls_data_dict, only_status_code=True)


def fetch_url(url_fetch_url, urls_data_dict):
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
    return post_store(url_fetch_url, urls_data_dict, only_status_code=True)
