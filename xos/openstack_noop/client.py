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
            self.username = controller.admin_user
            self.password = controller.admin_password
            self.tenant = controller.admin_tenant
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
	pass

    @require_enabled
    def connect(self, *args, **kwds):
        self.__init__(*args, **kwds)

    @require_enabled
    def authenticate(self):
	return True

