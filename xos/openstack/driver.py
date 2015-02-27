import commands
import hashlib
from xos.config import Config
from core.models import Controller

try:
    from openstack.client import OpenStackClient
    has_openstack = True
except:
    has_openstack = False

if has_openstack:
	from openstack_noop.driver import OpenStackDriver as OSDriver

manager_enabled = Config().api_nova_enabled

class OpenStackDriver(OSDriver):

    def __init__(self, config = None, client=None):
	OSDriver.__init__(self, config, client)

