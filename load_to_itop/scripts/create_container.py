from config import HTTP_PORT_MAP,MYSQL_PORT_MAP,CON_NAME,EXT_MAP,DUMP_MAP,IMAGE_NAME
import subprocess

cmd = "sudo docker run -d -p %s -p %s --name=%s -v %s -v %s %s" % (HTTP_PORT_MAP,MYSQL_PORT_MAP,CON_NAME,EXT_MAP,DUMP_MAP,IMAGE_NAME)
subprocess.call(cmd, shell=True)