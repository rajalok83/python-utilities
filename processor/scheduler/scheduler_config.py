import os
import django
import os
import sys
print(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'processor.settigns'
django.setup()
from datetime import datetime
from scheduler import models as smo

class SchedulerConfiguration:

  def create_scheduler_config(self, in_vndr_nm, in_prdct_typ, in_prdct_nm, in_prdct_ver, in_cnnct_dir, in_cnnct_strng) -> bool:
    curr_ts = datetime.now()
    t = smo.SchedulerConnectConfig(
      vndr_nm = in_vndr_nm, 
      prdct_typ = in_prdct_typ, 
      prdct_nm = in_prdct_nm, 
      prdct_ver = in_prdct_ver, 
      cnnct_dir = in_cnnct_dir, 
      cnnct_strng = in_cnnct_strng, 
      crt_ts = curr_ts, 
      updt_ts = curr_ts)
    t.save()
    return True

  def __str__(self) -> str:
    pass

  def __init__(self) -> None:
    pass


if __name__ == '__main__':
  s_cnfg = SchedulerConfiguration()
  s_cnfg.create_scheduler_config('Oracle', 'DB', 'Oracle', '19',
                              'H:\\TNSNAMES', 'SQLPLUS.EXE /{{ '@' }}{{ DBID }} {{ '@' }}{{ SCRPTFLPTH }}')