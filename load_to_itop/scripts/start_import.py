from config import CON_NAME,CON_IMP_SCRIPT
import batch_delete_all
import time
import subprocess
from urllib.error import HTTPError

restart_con= "sudo docker restart %s" % CON_NAME
ifexists_con="sudo docker ps | grep %s | wc -l" % CON_NAME
run_imp_script="sudo docker exec %s sh %s" % (CON_NAME,CON_IMP_SCRIPT)

def batch_delete():
    try:
        batch_delete_all.main(show=True)
    except HTTPError:
        batch_delete()

batch_delete()

print(subprocess.getoutput(restart_con))
time.sleep(5)
while True:
    if subprocess.getoutput(ifexists_con) == 0:    
        print("restrat not yet, retry")
    else:
        print("restart done")
        print("start import")
        print(run_imp_script)
        print(subprocess.getoutput(run_imp_script))
        break


