import commands
import hashlib
from xos.config import Config
from core.models import Controller

import sys
import traceback

try:
    from openstack.client import OpenStackClient
    has_openstack = True
except Exception,e:
    print "XXXXX: %s"%str(e)
    has_openstack = False

from openstack_noop.driver import OpenStackDriver as OSDriver

manager_enabled = Config().api_nova_enabled

class OpenStackDriver(OSDriver):

    def __init__(self, config = None, client=None):
	print ">>>> Creating OpenStack Driver: %s"%has_openstack
	OSDriver.__init__(self, config, client)

