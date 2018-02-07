import os

# set dir
WORKDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSVDIR = os.path.join(WORKDIR, 'csvfile')
SRCDIR = os.path.join(CSVDIR, 'source')
STATICDIR = os.path.join(CSVDIR, 'static')
DUMPDIR = os.path.join(CSVDIR, 'dump')


# source csv file
server_src_csv = os.path.join(SRCDIR, 'server_list.csv')
server_src_csv_vc06 = os.path.join(SRCDIR, 'server_list_vc06.csv')
server_src_csv_vc02 = os.path.join(SRCDIR, 'server_list_vc02.csv')
server_src_csv_ppvc06 = os.path.join(SRCDIR, 'server_list_ppvc06.csv')

vm_src_csv = os.path.join(SRCDIR, 'vm_list.csv')
vm_src_csv_vc06 = os.path.join(SRCDIR, 'vm_list_vc06.csv')
vm_src_csv_vc02 = os.path.join(SRCDIR, 'vm_list_vc02.csv')
vm_src_csv_ppvc06 = os.path.join(SRCDIR, 'vm_list_ppvc06.csv')


# static csv file
server_static_csv = os.path.join(STATICDIR, 'esx_server_static.csv')
nonesx_server_csv = os.path.join(STATICDIR, 'nonesx_server.csv')
network_csv = os.path.join(STATICDIR, 'networkdevice.csv')
storage_csv = os.path.join(STATICDIR, 'storagesystem.csv')
sync_ds_csv = os.path.join(STATICDIR, 'sync_data_source.csv')

# dump csv file
brand_csv = os.path.join(DUMPDIR, 'brand.csv')
model_csv = os.path.join(DUMPDIR, 'model.csv')
osfamily_csv = os.path.join(DUMPDIR, 'osfamily.csv')
osversion_csv = os.path.join(DUMPDIR, 'osversion.csv')
networktype_csv = os.path.join(DUMPDIR, 'networkdevicetype.csv')
physicalserver_csv = os.path.join(DUMPDIR, 'physicalserver.csv')
virtualmachine_csv = os.path.join(DUMPDIR, 'virtualmachine.csv')
hypervisor_csv = os.path.join(DUMPDIR, 'hypervisor.csv')

# container setting
IMAGE_NAME="vbkunin/itop:2.3.4"
CON_NAME = "itop0202"
# CON_NAME = "itop4"

HTTP_PORT = "80"
# HTTP_PORT = "8780"
MYSQL_PORT = "3319"
HTTP_PORT_MAP = "%s:%s" % (HTTP_PORT,'80')
MYSQL_PORT_MAP = "%s:%s" % (MYSQL_PORT,'3306')

EXTDIR = os.path.join(WORKDIR, 'itop-extension')
CON_EXTDIR = '/app/extensions'
CON_DUMPDIR = '/opt/dump'
EXT_MAP = "%s:%s" % (EXTDIR, CON_EXTDIR)
DUMP_MAP = "%s:%s" % (DUMPDIR, CON_DUMPDIR)

IMP_SCRIPT  = os.path.join(DUMPDIR,'import.sh')
CON_IMP_SCRIPT =os.path.join(CON_DUMPDIR,'import.sh')

# itop setting
API_URL="http://127.0.0.1:%s/webservices/rest.php" % HTTP_PORT
# API_URL="http://192.168.56.102:%s/webservices/rest.php" % HTTP_PORT
API_VER="1.3"
ITOP_USER="admin"
ITOP_PASS="Password1"

# itop sync data source config
models = (
# 'Organization',
'Environment',
'Location',
'Brand',
'Model',
'NetworkDeviceType',
'OSFamily',
'OSVersion',
'PhysicalServer',
'Hypervisor',
'VirtualMachine',
'NetworkDevice',
'StorageSystem',
)

