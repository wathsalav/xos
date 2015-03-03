import commands
import hashlib
from xos.config import Config
from core.models import Controller
import random
import uuid

try:
    from openstack.client import OpenStackClient
    has_openstack = True
except:
    has_openstack = False


manager_enabled = Config().api_nova_enabled

random.seed(None)


def get_random_int():
    return random.randint(1000,9999)

def get_random_uuid():
    return str(uuid.uuid4())

class OpenStackDriver:

    def __init__(self, config = None, client=None):
        if config:
            self.config = Config(config)
        else:
            self.config = Config()

        if client:
            self.shell = client

        self.enabled = manager_enabled
        self.has_openstack = has_openstack
        self.controller = None
        self.admin_user = None

    def client_driver(self, caller=None, tenant=None, controller=None):
        if caller:
            auth = {'username': caller.email,
                    'password': hashlib.md5(caller.password).hexdigest()[:6],
                    'tenant': tenant}
            client = OpenStackClient(controller=controller, cacert=self.config.nova_ca_ssl_cert, **auth)
        else:
            admin_driver = self.admin_driver(tenant=tenant, controller=controller)
            client = OpenStackClient(tenant=tenant, controller=admin_driver.controller)

        driver = OpenStackDriver(client=client)
        #driver.admin_user = admin_driver.admin_user
        #driver.controller = admin_driver.controller
        return driver

    def admin_driver(self, tenant=None, controller=None):
        if isinstance(controller, int):
            controller = Controller.objects.get(id=controller.id)
        client = OpenStackClient(tenant=tenant, controller=controller, cacert=self.config.nova_ca_ssl_cert)
        driver = OpenStackDriver(client=client)
        driver.admin_user = {'id': 'u0000', 'name' : 'admin', 'email' : 'admin@noop.controll.er', 'enabled': True}
        driver.controller = controller
        return driver    

    def create_role(self, name):
	return {'name': name, 'id': 'r'+str(get_random_int()), 'description': 'NoOp Admin'}
	
    def delete_role(self, filter):
        return 1

    def create_tenant(self, tenant_name, enabled, description):
        """Create keystone tenant. Suggested fields: name, description, enabled"""  
	tenant = {'id' : get_random_uuid(), 'name' : tenant_name, 'description' : description, 'enabled' : enabled}

        # always give the admin user the admin role to any tenant created 
        # by the driver. 
        self.add_user_role(self.admin_user.id, tenant.id, 'admin')
        return tenant

    def update_tenant(self, id, **kwds):
	tenant = {'id' : id, 'name' : kwds.get('name', 'NoOpTenant'), 'description' : kwds.get('description', 'A Tenant that has nothing to do with OpenStack'), 'enabled' : kwds.get('enabled', True)}
        return tenant 

    def delete_tenant(self, id):
        return 1

    def create_user(self, name, email, password, enabled):
	return {'id': 'u'+str(get_random_int()), 'name' : name, 'email' : email, 'enabled': enabled}


    def delete_user(self, id):
        return 1

    def get_admin_role(self):
	return {'name': name, 'id': 'r0000', 'description': 'NoOp Admin'}

    def add_user_role(self, kuser_id, tenant_id, role_name):
        return 1

    def delete_user_role(self, kuser_id, tenant_id, role_name):
        return 1 

    def update_user(self, id, fields):
        return 1 

    def create_router(self, name, set_gateway=True):
        # add router to external network
        if set_gateway:
	    router = {'status': 'ACTIVE',
	              'external_gateway_info': {'network_id': get_random_uuid()},
                      'name': 'NoOp-Router',
                      'admin_state_up': True,
                      'id': get_random_uuid()}
        else:
	    router = {'status': 'ACTIVE',
                      'name': 'NoOp-Router',
                      'admin_state_up': True,
                      'id': get_random_uuid()}
        return router

    def delete_router(self, id):
        return

    def add_router_interface(self, router_id, subnet_id):
	return

    def delete_router_interface(self, router_id, subnet_id):
	return
 
    def create_network(self, name, shared=False):
	net = {'status': 'ACTIVE',
               'subnets': [],
               'name': name,
               'admin_state_up': True,
               'shared': shared,
               'id': get_random_uuid()}
        return net
 
    def delete_network(self, id):
        return 1

    def delete_network_ports(self, network_id):
        return 1         

    def delete_subnet_ports(self, subnet_id):
        return 1
 
    def create_subnet(self, name, network_id, cidr_ip, ip_version, start, end):
        subnet = {'name': name,
                  'enable_dhcp': True,
                  'network_id': network_id,
                  'tenant_id': get_random_uuid(),
                  'dns_nameservers': [],
                  'allocation_pools': [{'start': start, 'end': end}],
                  'host_routes': [],
                  'ip_version': ip_version,
                  'gateway_ip': end,
                  'cidr': cidr_ip,
                  'id': get_randon_uuid()
                  }
        return subnet

    def update_subnet(self, id, fields):
        subnet = {'name': fields['name'],
                  'enable_dhcp': fields['enable_dhcp'],
                  'network_id': fields['network_id'],
                  'tenant_id': fields['tenant_id'],
                  'dns_nameservers': fields['dns_nameservers'],
                  'allocation_pools': fields['allocation_pools'],
                  'host_routes': fields['host_routes'],
                  'ip_version': fields['ip_version'],
                  'gateway_ip': fields['gateway_ip'],
                  'cidr': fields['cidr'],
                  'id': fields['id']
                  }
	return subnet

    def delete_subnet(self, id):
        return 1

    def get_external_routes(self):
        status, output = commands.getstatusoutput('route')
        routes = output.split('\n')[3:]
        return routes

    def add_external_route(self, subnet, routes=[]):
        return 1

    def delete_external_route(self, subnet):
        return 1
    
    def create_keypair(self, name, public_key):
        keys = self.shell.nova.keypairs.findall(name=name)
        if keys:
            key = keys[0]
            # update key     
            if key.public_key != public_key:
                self.delete_keypair(key.id)
                key = self.shell.nova.keypairs.create(name=name, public_key=public_key)
        else:
            key = self.shell.nova.keypairs.create(name=name, public_key=public_key)
        return key

    def delete_keypair(self, id):
        return 1

    def get_private_networks(self, tenant=None):
	return  [{'status': 'ACTIVE',
               'subnets': [],
               'name': "",
               'admin_state_up': True,
               'shared': True,
               'id': get_random_uuid()}]

    def get_shared_networks(self):
	return  [{'status': 'ACTIVE',
               'subnets': [],
               'name': "",
               'admin_state_up': True,
               'shared': True,
               'id': get_random_uuid()}]

    def get_network_subnet(self, network_id):
	subnet_id = get_random_uuid()
        subnet = {'name': name,
                  'enable_dhcp': True,
                  'network_id': network_id,
                  'tenant_id': get_random_uuid(),
                  'dns_nameservers': [],
                  'allocation_pools': [{'start': start, 'end': end}],
                  'host_routes': [],
                  'ip_version': ip_version,
                  'gateway_ip': end,
                  'cidr': cidr_ip,
                  'id': subnet_id
                  }
        return (subnet_id, subnet)

    def spawn_instance(self, name, key_name=None, availability_zone=None, hostname=None, image_id=None, security_group=None, pubkeys=[], nics=None, metadata=None, userdata=None, flavor_name=None):	
	server = {'security_groups': security_groups,
	          'OS-DCF:diskConfig': 'MAMAUL',
	          'id': get_random_uuid(),
	          'links': [],
	          'adminPass': 'password'
	         }
	return server

    def destroy_instance(self, id):
	return

    def update_instance_metadata(self, id, metadata):
	return

    def delete_instance_metadata(self, id, metadata):
        return

