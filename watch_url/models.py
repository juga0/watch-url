

class StoreConfigPagesDoc(object):
    """{
    u'_rev': u'1-cc1b76687b6b3319d18dca4e3e29117a',
    u'_id': u'pages-juga',
    u'config':,
        [{u'policy': u'privacy_policy',
        u'organization': u'theguardianproject',
        u'tool': u'chatsecure',
        u'url': u'https://guardianproject.info/home/data-usage-and-protection-policies/',
        u'xpath': u'//article'},
    ]}
    """

    def __init__(self, id_doc=AGENT_NAME):
        _rev = ''
        _id = ''
        config = []

    def loads(self, text):
        args = json.loads(stream)
        self.__dict__.update(args)

    def get_store_config_doc(self, store_config_url=STORE_CONFIG_URL):
        # get_store()
        args_text = get_store_rules(store_config_url)
        self.loads(args_text)


class StoreConfigPagesField(object):
    """
    u'policy': u'privacy_policy',
    u'organization': u'theguardianproject',
    u'tool': u'chatsecure',
    u'url': u'https://guardianproject.info/home/data-usage-and-protection-policies/',
    u'xpath': u'//article'
    """
    policy = 'privacy_policy'
    organization = 'theguardianproject'
    tool = 'chatsecure'
    url = 'https://guardianproject.info/home/data-usage-and-protection-policies/'
    xpath = '//article'

    def get_config_field(self):
        pass


class Header(object):
    etag = None
    last_modified = None

    def get_page_header(self):
        # get_etag
        pass


class PagesPayload(object):
    """{
    'xpath': u'//article',
    'agent_ip': '78.142.19.213',
    'content': '',
    'header': {
        'etag': None,
        'last_modified': None},
    'agent_type': 'watch',
    'key': u'https://guardianproject.info/home/data-usage-and-protection-policies/',
    'timestamp_measurements': '20160729T231315Z'}
    }"""
    agent_ip = '78.142.19.213'
    header = None
    agent_type = 'watch'
    key = 'https://guardianproject.info/home/data-usage-and-protection-policies/'
    timestamp_measurements = '20160729T231315Z'
    xpath = '//article'

    def gen_doc_id(self):
        pass

    def post_pages_update(self):
        # post_store()
        pass

    def get_latest_pages_view(self):
        # get_store_etag
        pass

class PagesService(object):
    store_config_url = STORE_CONFIG_URL
    config_doc = {}
    rules = []
    rule = None
    page_url = ''

    def __init__(self, store_config_url=STORE_CONFIG_URL):
        store_config_url = store_config_url
        rules = []
        rule = None
        page_url = ''

    def get_config(self):
        config_doc = StoreConfigPagesDoc()
        config_doc.get_store_config_doc(self.store_config_url)

    def do(self):
        # get config
        # iterate rules
        # get etag from store
        # get etag from page
        # compare etags, if differents
        # generate doc id
        # generate payloa
        # store payload
        # get fetch
        pass
