import urllib.request
import urllib.parse
import json
from pprint import pprint
from config import API_URL, API_VER, ITOP_USER, ITOP_PASS

def http_post(opr):
    url="%s?version=%s" % (API_URL,API_VER)
    auth ={"auth_user": ITOP_USER , "auth_pwd": ITOP_PASS}
    oprjson =urllib.parse.urlencode({'json_data': json.dumps(opr)})
    jdata = urllib.parse.urlencode(auth)
    jdata = jdata+'&'+oprjson
    response = urllib.request.urlopen(url,jdata.encode(encoding='UTF8'))
    return response.read()

def main(show=False):
    class_list = [
    'lnkVirtualDeviceToVolume',
    'lnkServerToVolume',
    'LogicalVolume',
    'MongoDBInstance',
    'DatabaseSchema',
    'DBServer',
    'NginxInstance',
    'OHSInstance',
    'SpotfireInstance',
    'SpotfireWebInstance',
    'BWInstance',
    'EMSInstance',
    'OC4JInstance',
    'SolrInstance',
    'WeblogicInstance',
    'GFSInstance',
    'ZooKeeperInstance',
    'WebServer',
    'MiddlewareInstance',
    'Middleware',
    'StorageSystem',
    'VirtualMachine',
    'Hypervisor',
    'Server',
    'PhysicalServer',
    'NetworkDevice',
    'NetworkDeviceType',
    'LogicalVolume',
    'OSVersion',
    'OSFamily',
    'Model',
    'Brand',
    'ApplicationSolution',
    'Location',
    'Environment',
    ]
    
    for class_name in class_list:
        key_name = "SELECT {class_name}".format(class_name=class_name)
        opr={
            "operation": "core/delete",
            "comment": "Cleanup for customer Demo",
            "class": "{class_name}".format(class_name=class_name),
            "key":"{key}".format(key=key_name),
            "simulate": False
        }
    
        rep=http_post(opr)
        if show:
            pprint(rep)
        pprint("deleted {class_name}".format(class_name=class_name))

if __name__ == '__main__':
    main(show=True)
