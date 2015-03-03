import urlparse

'''
This is a temp hack! 
Load openstack_noop or openstack_real at runtim based on configuration...
'''
is_openstack_noop = True

from openstack_noop.client import OpenStackClient as OSClient
from openstack_noop.client import KeystoneClient as KSClient
from openstack_noop.client import Glance as GlanceObject
from openstack_noop.client import GlanceClient as GClient
from openstack_noop.client import NovaClient as NClient
from openstack_noop.client import NovaDB as NovaDBObject
from openstack_noop.client import QuantumClient as QClient

from xos.config import Config


has_openstack = True

def require_enabled(callable):
    def wrapper(*args, **kwds):
        if has_openstack:
            return callable(*args, **kwds)
        else:
            return None
    return wrapper

def parse_novarc(filename):
    opts = {}
    f = open(filename, 'r')
    for line in f:
        try:
            line = line.replace('export', '').strip()
            parts = line.split('=')
            if len(parts) > 1:
                value = parts[1].replace("\'", "")
                value = value.replace('\"', '')
                opts[parts[0]] = value
        except:
            pass
    f.close()
    return opts

class KeystoneClient(KSClient):
    def __init__(self, *args, **kwds):
        KSClient.__init__(self, *args, **kwds)

class Glance(GlanceObject):
    def __init__(self, *args, **kwds):
        GlanceObject.__init__(self, *args, **kwds)

class GlanceClient(GClient):
    def __init__(self, version, endpoint, token, cacert=None, *args, **kwds):
        GClient.__init__(self, *args, **kwds)

class NovaClient(NClient):
    def __init__(self, *args, **kwds):
        NClient.__init__(self, *args, **kwds)

class NovaDB(NovaDBObject):
    def __init__(self, *args, **kwds):
        NovaDBObject.__init__(self, *args, **kwds)

class QuantumClient(QClient):
    def __init__(self, *args, **kwds):
        QClient.__init__(self, *args, **kwds)

class OpenStackClient(OSClient):
    """
    A simple native shell to the openstack backend services.
    This class can receive all nova calls to the underlying testbed
    """

    def __init__ ( self, *args, **kwds) :
        # instantiate managers
	OSClient.__init__(self, *args, **kwds)
        self.keystone = KeystoneClient(*args, **kwds)
        url_parsed = urlparse.urlparse(self.keystone.url)
        hostname = url_parsed.netloc.split(':')[0]
	#if not is_openstack_noop:
        #	token = self.keystone.client.tokens.authenticate(username=self.keystone.username, password=self.keystone.password, tenant_name=self.keystone.tenant)
        #	glance_endpoint = self.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
        #	self.glanceclient = GlanceClient('1', endpoint=glance_endpoint, token=token.id, **kwds)
        #else:
        #	self.glanceclient = GlanceClient('1', endpoint="", token=None, **kwds)
        #self.nova = NovaClient(*args, **kwds)
        #self.nova_db = NovaDB(*args, **kwds)
        self.quantum = QuantumClient(*args, **kwds)
    

    @require_enabled
    def connect(self, *args, **kwds):
        self.__init__(*args, **kwds)

    @require_enabled
    def authenticate(self):
        return self.keystone.authenticate()

