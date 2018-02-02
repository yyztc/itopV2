#encoding=utf8

import shutil
import csv
import os
import numpy as np
import pandas as pd
from pprint import pprint
from config import server_src_csv, vm_src_csv, server_static_csv, network_csv, storage_csv, sync_ds_csv, brand_csv, model_csv, osfamily_csv, osversion_csv, networktype_csv, physicalserver_csv, virtualmachine_csv, hypervisor_csv, nonesx_server_csv
from config import DUMPDIR,STATICDIR


def format_osfamily_name(osversion_name):
    if 'WINDOW' in osversion_name.upper():
        osfamily_name = 'WINDOWS'
    elif 'RED' in osversion_name.upper():
        osfamily_name ='REDHAT'
    elif 'CENTOS' in osversion_name.upper():
        osfamily_name='CENTOS'
    elif 'ESX' in osversion_name.upper():
        osfamily_name='ESX'
    else:
        osfamily_name='OTHERS'
    return osfamily_name
   

def format_server(server_df,csvfile):

    # rename column name
    columns = {
    'vc_model_name':'model_id', 
    'vc_cpu_speedGHz':'cpu_speed', 
    'vc_os_version':'osversion_id', 
    'vc_memory_size':'memory', 
    'vc_cpu_num':'cpu_num', 
    'vc_power_status':'power_status', 
    'vc_env':'env_id', 
    'vc_fiber_hba_num':'fiber_card_num', 
    'vc_brand_name':'brand_id', 
    'vc_cpu_type':'cpu_type', 
    'vc_name':'name',
    'vc_ip':'ip',
    'vc_cpu_core':'cpu_core',
    'vc_fiber_hba_device':'fiber_card_model'
    }
    server_df = server_df.rename(columns=columns).assign(org_id=lambda x:'Cargosmart').assign(business_criticity=lambda x:'high').assign(status='production').assign(server_type='ESX')[['model_id','cpu_speed','osversion_id','memory','cpu_num','power_status','env_id','fiber_card_num','brand_id','cpu_type','name','org_id','business_criticity','cpu_core','ip','fiber_card_model','status','server_type']]

    # add osfmaily
    server_df['osfamily_id'] = server_df['osversion_id'].map(lambda x:format_osfamily_name(x))

    # join with static data
    server_df['join_name']=server_df['name'].map(lambda x:x.lower().split('.cargosmart.com')[0])
    df = pd.merge(server_df, server_static_df, left_on='join_name',right_on='server_name').drop(['join_name','server_name'], axis=1)

    # union nonesx server
    df = pd.concat([df,nonesx_server_df])

    # format name without domain
    df['name'] = df['name'].map(lambda x:x.split('.')[0].lower())

    # add primary key
    df.index=[x for x in range(len(df))]
    df['primary_key'] = df.index+1
    df.set_index('primary_key',inplace=True)

    df.to_csv(csvfile)
    return df

def format_vm(vm_df,csvfile):

    columns = {
    'vc_name': 'name',
    'vc_memory_size': 'ram',
    'vc_cpu_num': 'cpu',
    'vc_ip': 'ip',
    'vc_server_name': 'virtualhost_id',
    'vc_env': 'env_id',
    'vc_vm_os_version': 'osversion_id',
    'vc_power_status': 'powerState',
    }

    vm_df = vm_df.rename(columns=columns).assign(org_id=lambda x:'Cargosmart').assign(business_criticity=lambda x:'high')[['name','ram','cpu','ip','virtualhost_id','env_id','osversion_id','powerState','org_id','business_criticity']]

    # add osfmaily
    vm_df['osfamily_id'] = vm_df['osversion_id'].map(lambda x:format_osfamily_name(x))

    # format name without domain
    vm_df['name']=vm_df['name'].map(lambda x:x.split('.')[0].lower())
    vm_df['virtualhost_id']=vm_df['virtualhost_id'].map(lambda x:x.split('.')[0].lower())

    # add primary key
    vm_df.index=[x for x in range(len(vm_df))]
    vm_df['primary_key'] = vm_df.index+1
    vm_df.set_index('primary_key',inplace=True)

    vm_df.to_csv(csvfile)
    return vm_df    

def gen_brand_csv(server_df,network_df,csvfile):
    server_brand=server_df['model_id'].map(lambda x:x.split()[0]).drop_duplicates().rename('name')
    network_brand = network_df.brand_id.drop_duplicates().rename('name')
    storage_brand = storage_df.brand_id.drop_duplicates().rename('name')

    merge_brand = server_brand.append(network_brand).append(storage_brand).drop_duplicates()
    df = pd.DataFrame(merge_brand).reset_index(drop=True)
    df.index=[x for x in range(len(df))]
    df['primary_key']=df.index+1
    df.set_index('primary_key',inplace=True)
    df.to_csv(csvfile)
    return df

def gen_model_csv(server_df,network_df,csvfile):
    server_model = server_df.assign(type=lambda x:'Server').drop(['name'], axis=1).rename(columns={'model_id':'name'})[['name','type','brand_id']].drop_duplicates()
    network_model = network_df.assign(type=lambda x:'NetworkDevice').drop(['name'], axis=1).rename(columns={'model_id':'name'})[['name','type','brand_id']].drop_duplicates()
    storage_model = storage_df.assign(type=lambda x:'StorageSystem').drop(['name'], axis=1).rename(columns={'model_id':'name'})[['name','type','brand_id']].drop_duplicates()

    merge_model = server_model.append(network_model).append(storage_model)
    # df = pd.DataFrame(merge_model).reset_index(drop=True)
    df = pd.DataFrame(merge_model)
    df.index=[x for x in range(len(df))]
    df['primary_key'] = df.index+1
    df.set_index('primary_key',inplace=True)
    df.to_csv(csvfile)
    return df

def gen_osfamily_csv(server_df,vm_df,csvfile):
    server_osfamily = server_df['osfamily_id'].drop_duplicates().rename('name')
    vm_osfamily =  vm_df['osfamily_id'].drop_duplicates().rename('name')

    merge_osfamily = server_osfamily.append(vm_osfamily)
    # df = pd.DataFrame(merge_osfamily).reset_index(drop=True)
    df = pd.DataFrame(merge_osfamily)
    df.index=[x for x in range(len(df))]
    df['name']=df['name'].map(lambda x:str(x).strip())
    df=df.loc[df['name'] != ''].loc[df['name']!='nan']
    df['primary_key'] = df.index+1
    df.set_index('primary_key',inplace=True)
    df.to_csv(csvfile)
    return df

def gen_osversion_csv(server_df,vm_df,csvfile):
    server_osversion = server_df.drop(['name'], axis=1).rename(columns={'osversion_id':'name'})[['name','osfamily_id']].drop_duplicates()
    vm_osversion = vm_df.drop(['name'], axis=1).rename(columns={'osversion_id':'name'})[['name','osfamily_id']].drop_duplicates()

    merge_osversion = server_osversion.append(vm_osversion)
    merge_osversion = merge_osversion.loc[merge_osversion['name'].notnull()]
    # df = pd.DataFrame(merge_osversion).reset_index(drop=True)
    df = pd.DataFrame(merge_osversion)
    df.index=[x for x in range(len(df))]
    df['primary_key'] = df.index+1
    df.set_index('primary_key',inplace=True)
    df.to_csv(csvfile)
    return df

def gen_networktype_csv(network_df,csvfile):
    networktype=network_df.networkdevicetype_id.drop_duplicates().rename('name')
    # df = pd.DataFrame(networktype).reset_index(drop=True)
    df = pd.DataFrame(networktype)
    df.index=[x for x in range(len(df))]
    df['primary_key'] = df.index+1
    df.set_index('primary_key',inplace=True)
    df.to_csv(csvfile)
    return df

def gen_hypervisor_csv(server_df,csvfile):
    df = server_df[['name','org_id','env_id','business_criticity','status']].assign(server_id=lambda x:x['name'])
    df.to_csv(csvfile)
    return df


if __name__ == '__main__':

    server_src_df = pd.DataFrame(pd.read_csv(server_src_csv))
    vm_src_df = pd.DataFrame(pd.read_csv(vm_src_csv))
    server_static_df = pd.DataFrame(pd.read_csv(server_static_csv))
    nonesx_server_df = pd.DataFrame(pd.read_csv(nonesx_server_csv)) 
    network_df = pd.DataFrame(pd.read_csv(network_csv))
    storage_df = pd.DataFrame(pd.read_csv(storage_csv))

    # format data
    server_df = format_server(server_src_df,physicalserver_csv)    
    vm_df = format_vm(vm_src_df,virtualmachine_csv)    

    # gen csv
    gen_brand_csv(server_df,network_df,brand_csv)
    gen_model_csv(server_df,network_df,model_csv)
    gen_osfamily_csv(server_df,vm_df,osfamily_csv)
    gen_osversion_csv(server_df,vm_df,osversion_csv)
    gen_networktype_csv(network_df,networktype_csv)
    gen_hypervisor_csv(server_df,hypervisor_csv)

    # copy static csv file to dump dir
    static_files = os.listdir(STATICDIR)
    for filename in static_files:
        src =  os.path.join(STATICDIR,filename)
        dst = os.path.join(DUMPDIR,filename)
        if os.path.exists(dst):
            os.remove(dst)
        shutil.copyfile(src,dst)



