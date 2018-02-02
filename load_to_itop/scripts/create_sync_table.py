from pprint import pprint
import os
import itopy
from config import sync_ds_csv,API_URL, API_VER, ITOP_USER, ITOP_PASS
from config import DUMPDIR,CON_DUMPDIR,IMP_SCRIPT
from config import models
import collections
    
def create_sync_table():
    itop = itopy.Api()
    itop.connect(API_URL, API_VER, ITOP_USER, ITOP_PASS)
    
    model_sourceid = collections.OrderedDict()
    
    for model in models:
        sync_ds_name = "%s from csv" % model.lower()
        res = itop.create('SynchroDataSource',
        name=sync_ds_name,
        scope_class=model,
        status='production',
        reconciliation_policy='use_attributes',
        # reconciliation_policy='use_primary_key',
        action_on_zero='create',
        action_on_one='update',
        action_on_multiple='error',
        delete_policy='ignore',
        user_delete_policy='administrators'
        )
        if res.get('message') is None:
            data_source_id = res.get('item_key')[0]
            model_sourceid[model]=data_source_id
    return model_sourceid


def create_import_script(model_sourceid):
    cmd = ''
    with open(IMP_SCRIPT,'w') as f:
        for model ,sourceid in model_sourceid.items():
            csvfilename = model.lower() + '.csv'
            csvfile=os.path.join(CON_DUMPDIR,csvfilename)
            cmd += "php -q /app/synchro/synchro_import.php  --auth_user=%s --auth_pwd=%s    --data_source_id=%s     --csvfile=%s --separator=,\n" % (ITOP_USER,ITOP_PASS,  sourceid,csvfile)
        f.writelines(cmd)


model_sourceid = create_sync_table()
pprint(model_sourceid)
create_import_script(model_sourceid)

