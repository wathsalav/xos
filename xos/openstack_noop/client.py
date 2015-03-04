import urlparse
import random
import uuid

from xos.config import Config

from keystoneclient import service_catalog

has_openstack = True
random.seed(None)

def require_enabled(callable):
    def wrapper(*args, **kwds):
        if has_openstack:
            return callable(*args, **kwds)
        else:
            return None
    return wrapper

def parse_novarc(filename):
    opts = {}
    return opts

ef get_random_int():
    return random.randint(1000,9999)

def get_random_uuid():
    return str(uuid.uuid4())


class Client:
    def __init__(self, username=None, password=None, tenant=None, url=None, token=None, endpoint=None, controller=None, admin=True, *args, **kwds):
       
        self.has_openstack = has_openstack
        self.url = controller.auth_url
        if admin:
            self.username = "admin"#controller.admin_user
            self.password = ""#controller.admin_password
            self.tenant = "tenant0"#controller.admin_tenant
        else:
            self.username = None
            self.password = None
            self.tenant = None

        if username:
            self.username = username
        if password:
            self.password = password
        if tenant:
            self.tenant = tenant
        if url:
            self.url = url
        if token:
            self.token = token    
        if endpoint:
            self.endpoint = endpoint

        #if '@' in self.username:
        #    self.username = self.username[:self.username.index('@')]

class DummyClient:
    def __init__(self, client_name):
        self.client = client_name
        self.service_catalog = service_catalog.ServiceCatalogV2({})
        self.images = DummyImages()

    def list_ports(self, retrieve_all=True, **_params):
        return {'ports': [{'id': 'port0', 'device_owner': 'compute:nova',
                                'device_id': 'dev0', 'network_id': 'net0', 'fixed_ips': None},
                          {'id': 'port1', 'device_owner': 'compute:nova',
                                'device_id': 'dev1', 'network_id': 'net1', 'fixed_ips': None}]}

    def list_networks(self):
        return {'networks': [{'id': 'net0', 'name': 'network-0'},
                             {'id': 'net1', 'name': 'network-1'}]}

class DummyImage:
    def __init__(self):
        self.name = 'test.img'
        self.id = 'c41c1b90-c2ac-11e4-8dfc-aa07a5b093db'

class DummyImages:
    def __init__(self):
        pass

    def list(self):
        return [DummyImage()]


class KeystoneClient(Client):
    def __init__(self, *args, **kwds):
        Client.__init__(self, *args, **kwds)
	self.client = DummyClient("KeystoneClient-%s"%get_random_uuid())
	

    @require_enabled
    def connect(self, *args, **kwds):
        self.__init__(*args, **kwds)

    @require_enabled
    def __getattr__(self, name):
        return getattr(self.client, name)


class Glance(Client):
    def __init__(self, *args, **kwds):
        Client.__init__(self, *args, **kwds)
	self.client = DummyClient("Glance-%s"%get_random_uuid())

    @require_enabled
    def __getattr__(self, name):
        return getattr(self.client, name)

class GlanceClient(Client):
    def __init__(self, version, endpoint, token, cacert=None, *args, **kwds):
        Client.__init__(self, *args, **kwds)
	self.client = DummyClient("GlanceClient-%s"%get_random_uuid())

    @require_enabled
    def __getattr__(self, name):
        return getattr(self.client, name)        

class NovaClient(Client):
    def __init__(self, *args, **kwds):
        Client.__init__(self, *args, **kwds)
	self.client = DummyClient("NovaClient-%s"%get_random_uuid())

    @require_enabled
    def connect(self, *args, **kwds):
        self.__init__(*args, **kwds)

    @require_enabled
    def __getattr__(self, name):
        return getattr(self.client, name)

class NovaDB(Client):
    def __init__(self, *args, **kwds):
        Client.__init__(self, *args, **kwds)
	self.client = DummyClient("NovaDB-%s"%get_random_uuid())

    @require_enabled
    def connect(self, *args, **kwds):
        self.__init__(*args, **kwds)

    @require_enabled
    def __getattr__(self, name):
        return getattr(self.client, name)

class QuantumClient(Client):
    def __init__(self, *args, **kwds):
        Client.__init__(self, *args, **kwds)
	self.client = DummyClient("QuantumClient-%s"%get_random_uuid())

    @require_enabled
    def connect(self, *args, **kwds):
        self.__init__(*args, **kwds)

    @require_enabled
    def __getattr__(self, name):
        return getattr(self.client, name)

class OpenStackClient:
    """
    A simple native shell to the openstack backend services.
    This class can receive all nova calls to the underlying testbed
    """

    def __init__ ( self, *args, **kwds) :
        #self.keystone = KeystoneClient(*args, **kwds)
        #url_parsed = urlparse.urlparse(self.keystone.url)
        #hostname = url_parsed.netloc.split(':')[0]
        #token = self.keystone.client.tokens.authenticate(username=self.keystone.username, password=self.keystone.password, tenant_name=self.keystone.tenant)
        #glance_endpoint = self.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')

        self.glanceclient = GlanceClient('1', endpoint="", token="", **kwds)
        self.nova = NovaClient(*args, **kwds)
        # self.nova_db = NovaDB(*args, **kwds)
        self.quantum = QuantumClient(*args, **kwds)
	

    @require_enabled
    def connect(self, *args, **kwds):
        self.__init__(*args, **kwds)

    @require_enabled
    def authenticate(self):
	return True

