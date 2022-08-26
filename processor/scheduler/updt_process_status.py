from datetime import datetime
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'processor.settings'
django.setup()
from scheduler import models as smo


def add_schedule(in_pid, in_uid, in_tag, in_cnnct_id, in_tmplt_id, in_cnnct_cntxt, in_status):
  # models.SchedulerProcess.objects.all().delete()
  curr_ts = datetime.now()
  schd_proc_mo = smo.SchedulerProcess(
    pid=in_pid, uid=in_uid, tag=in_tag, cnnct_id=in_cnnct_id, tmplt_id=in_tmplt_id, cnnct_cntxt=in_cnnct_cntxt, status=in_status, crt_ts=curr_ts, updt_ts=curr_ts)
  schd_proc_mo.save()
  return


def upd_schedule(in_uid, in_status):
  # models.SchedulerProcess.objects.all().delete()
  curr_ts = datetime.now()
  smo.SchedulerProcess.objects.filter(
    uid=in_uid).update(status=in_status, updt_ts=curr_ts)

  return
