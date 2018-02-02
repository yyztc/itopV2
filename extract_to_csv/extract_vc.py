import json
import logging
from logging.config import fileConfig
from models.vc import VC
import configparser
import argparse
import os
from ftplib import FTP
import time
import json_to_csv as jc

BASE_DIR = os.path.dirname(__file__)
DUMP_DIR = os.path.join(BASE_DIR,'dump')
CONFIG_FILE = os.path.join(BASE_DIR,'config.ini')
fileConfig('logger_config.ini')
logger = logging.getLogger('infoLogger')


def extract_data(host, user, passwd, port):
    vc = VC(host, user, passwd, port)
    logger.info("start extract %s" % host)
    vc_objects = {}
    server_list = []
    vm_list = []
    ds_list = []
    license_list = []
    for dc in vc.get_data_center_list():
        server_list += vc.get_server_list(dc)
        vm_list += vc.get_vm_list(dc)
        ds_list += vc.get_ds_list(dc)
        license_list += vc.get_license_list()
    vc_objects['server_list'] = server_list
    vc_objects['vm_list'] = vm_list
    vc_objects['ds_list'] = ds_list
    vc_objects['license_list'] = license_list
    logger.info("done")
    return vc_objects

def gen_filename(object_name,data_src):
    opt_time = time.strftime('%Y%m%d',time.localtime(time.time()))
    filename = "%s_%s_%s.json" % (object_name, data_src, opt_time)
    return filename


def to_json(data,filename):
    filepath = os.path.join(DUMP_DIR,filename)
    logger.info("start dump to json: %s" % filepath)
    with open(filepath,'w') as wf:
        wf.write(json.dumps(data))
    logger.info("done")


def ftp_upload(filename):
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE)
    config_item = 'csftp'
    (host, user, passwd, remotedir) = (
        cfg.get(config_item, "host"), 
        cfg.get(config_item, "user"), 
        cfg.get(config_item, "passwd"),
        cfg.get(config_item, "remotedir")
        )
    remotepath = os.path.join(remotedir,filename)
    localpath = os.path.join(DUMP_DIR,filename)

    ftp = FTP()
    ftp.connect(host, port=21)
    ftp.login(user, passwd)
    bufsize = 1024
    fp = open(localpath, 'rb')
    logger.info("start upload from %s to %s" % (localpath,remotepath))
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()
    logger.info("done")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    args = parser.parse_args()

    if args.host:
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG_FILE)
        config_item = args.host
        (host, user, passwd, port) = (cfg.get(config_item, "host"), cfg.get(
            config_item, "user"), cfg.get(config_item, "passwd"), cfg.get(config_item, "port"))

        vc_objects = extract_data(host, user, passwd, port)

        for object_name,data in vc_objects.items():
            json_filename = gen_filename(object_name=object_name,data_src = args.host)
            to_json(data=data, filename=json_filename)
            jc.convert_json_to_csv(json_filepath=os.path.join(DUMP_DIR,json_filename))
            ftp_upload(filename=os.path.splitext(json_filename)[0] + '.csv')
