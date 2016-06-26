"""watch_url functions that depends on the CouchDB scheme"""
# from couchdbkit import *
import requests
import sys
import logging
from config import AGENT_ID

logger = logging.getLogger(__name__)


# class Rule(Document):
#     url = StringProperty()
#     xpath = StringProperty()
#     organization = StringProperty()
#     policy = StringProperty()
#     tool = StringProperty()
#     # last_updated = DateTimeProperty()
#
#
# class ConfigRules(Document):
#     config = ListProperty(item_type=list)
#
#
# def connect_db(couchdb_url, db, doc, use_proxy=False):
#     s = Server(couchdb_url, use_proxy=use_proxy)
#     db_conn = s.get_or_create_db(db)
#     return db_conn
#
#
# def get_confrules_couchdbkit(db_conn, doc_url):
#     ConfigRules.set_db(db_conn)
#     confrules = ConfigRules()
#     confrules.get(doc_url)
#     rules = confrules['config']
#     return rules


def get_db_rules(doc_url):
    logger.debug('doc_url %s' % doc_url)
    r = requests.get(doc_url)
    confrules = r.json()
    # logger.debug('confrules %s' % confrules)
    rules = confrules.get('config')
    return rules


def get_db_etag(etag_url):
    logger.debug('etag_url %s', etag_url)
    r = requests.get(etag_url)
    # TODO: manage conflict when status code 409
    # logger.debug('get db etag response %s', r.json())
    etag = last_modified = ''
    if r.json().get("rows"):
        try:
            etag = r.json()['rows'][0]['value']['header'].get('etag')
            last_modified = r.json()['rows'][0]['value']['header'].get('last-modified')
        except KeyError, IndexError:
            logger.debug('no key etag or/nor last_modified in db')
    logger.debug('etag %s', etag)
    logger.debug('last-modified %s', last_modified)
    return etag, last_modified


def put_db_etag(url_db, url, etag='', last_modified=''):
    """{"_id":"tos-1","_rev":"2-cc47e0deb5b8efb2cf81b635c7790f03","key":"https://www.whispersystems.org/signal/privacy/","agent_id":"agent-tos-1","header":{"etag":"","last-modified":"Mon, 13 Jun 2016 19:01:36 GMT"},"content":"# Privacy Policy\n\nSignal provides end-to-end encrypted calling and messaging. We cannot decrypt\nor otherwise access the content of a call or a message.\n\n## Information We Have\n\nCertain information (e.g. a recipient's identifier, an encrypted message body,\netc.) is transmitted to us solely for the purpose of placing calls or\ntransmitting messages. Unless otherwise stated below, this information is only\nkept as long as necessary to place each call or transmit each message, and is\nnot used for any other purpose.\n\n### 1. Information we store\n\n  * The phone number or identifier you register with.\n\n  * Randomly generated authentication tokens, keys, push tokens, etc. necessary for setting up a call or transmitting a message.\n\n  * Profile information (e.g. an avatar, etc) you submit.\n\n### 2. Transient information\n\n  * IP addresses may be kept in memory for rate limiting or to prevent abuse.\n\n  * Information from the contacts on your device may be cryptographically hashed and transmitted to the server in order to [determine which of your contacts are registered](/blog/contact-discovery).\n\n## Information We May Share\n\nWe do not share your information with companies, organizations, and\nindividuals outside of OWS unless one of the following circumstances applies:\n\n  * With your consent.\n\n  * Through normal communication with a federated server operated by another entity. Some Signal users might be registered with other providers (e.g. CyanogenMOD), which requires passing messages, synchronizing views of registered users, etc.\n\n  * When legally required.\n\nWe will share the information we have with entities outside of OWS if we have\na good faith belief that access, use, preservation, or disclosure of the\ninformation is necessary to:\n\n  * meet any applicable law, regulation, legal process or enforceable governmental request.\n  * enforce applicable Terms of Service, including investigation of potential violations.\n  * detect, prevent, or otherwise address fraud, security, or technical issues.\n  * protect against harm to the rights, property, or safety of OWS, our users, or the public as required or permitted by law.\n\nWe will update this privacy policy as needed so that it is current, accurate,\nand as clear as possible.\n\n"}"""
    data = {
        "key": url,
        "agent_id": AGENT_ID,
        "header": {
            "etag": etag,
            "last-modified": last_modified
        },
        "content": ""
    }
    logger.debug('put url %s with etag %s and last-modified %s' % (url, etag, last_modified))
    # TODO: generate id?
    # To create new document you can either use a POST operation or a PUT operation. To create/update a named document using the PUT operation
    # To update an existing document, you also issue a PUT request. In this case, the JSON body must contain a _rev property, which lets CouchDB know which revision the edits are based on. If the revision of the document currently stored in the database doesn't match, then a 409 conflict error is returned.
    # It is recommended that you avoid POST when possible, because proxies and other network intermediaries will occasionally resend POST requests, which can result in duplicate document creation. If your client software is not capable of guaranteeing uniqueness of generated UUIDs, use a GET to /_uuids?count=100 to retrieve a list of document IDs for future PUT requests. Please note that the /_uuids-call does not check for existing document ids; collision-detection happens when you are trying to save a document.
    # FIXME: manage conflict
    r = requests.put(url_db, json=data)
    logger.debug('put request to url %s returned status %s', url_db, r.status_code)
    return r.status_code


def fetch_url(url_fetch_url, url, etag='', last_modified=''):
    data = {
        "key": url,
        "agent_id": AGENT_ID,
        "header": {
            "ETag": etag,
            "Last-Modified": last_modified
        },
        "content": ""
    }
    logger.debug('post url %s with etag %s and last-modified %s' % (url, etag, last_modified))
    r = requests.post(url_fetch_url, json=data)
    return r.status_code
