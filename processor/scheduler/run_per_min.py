from datetime import datetime
import json
import subprocess
from time import sleep
import traceback
import uuid
import psutil
from subprocess import Popen as po
from jinja2 import Template
from tempfile import gettempdir
import django
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'processor.settings'
django.setup()
import updt_process_status
from template import models as tmo
from scheduler import models as smo


class RunPerMin:
  all_arg = []
  in_type = None
  run_end_typ = None
  runs_per_min = 1
  session_typ = None
  in_list = []
  limit_sessions = 3
  max_sessions = 10
  all_active_proc = []
  tempdir = gettempdir()

  def get_process_status(self):
    for proc in self.all_active_proc:
      try:
        p = psutil.Process(proc.pid)
        print('{}->{}->{}'.format(proc, str(proc.pid), str(p.status())))
        all_child_process_completed = True
        for cproc in p.children():
          if not all_child_process_completed:
            break
          cp = psutil.Process(cproc.pid)
          print('CP:{}->{}->{}->{}'.format(proc.pid,
                cproc, str(cproc.pid), str(cp.status())))
          if cp.status() == psutil.STATUS_RUNNING:
            all_child_process_completed = False
          else:
            lines = cproc.stderr.readlines()
            for line in lines:
              print('CPROC:Error->{}->{}'.format(cproc.pid, str(line.rstrip())))
      except psutil.NoSuchProcess:
        proc_uid = proc.args.split(' ')[1]
        # print(proc_uid)
        self.updt_proc_status(proc_uid, 'N/A', 'Completed')
        self.all_active_proc.remove(proc)
        out_file = '{}{}{}'.format(self.tempdir, os.path.sep, proc_uid)
        with open('{}.log'.format(out_file), 'r') as log_file:
          log_data = log_file.readlines()
          # print("Log File --------------{}-------------".format(proc_uid))
          # print(log_data)
          # log_file.seek(0)
          # print(len(log_data))
          joined_log_data = ("\n").join(log_data).upper()
          if joined_log_data.find("ERROR".format(proc_uid)) > -1:
            self.updt_proc_status(proc_uid, 'N/A', 'Completed - Error')
          elif joined_log_data.find("{} SUCCESSFUL".format(proc_uid)) > -1:
            self.updt_proc_status(proc_uid, 'N/A', 'Successful')
          else:
            with open('{}.err'.format(out_file), 'r') as err_file:
              err_data = err_file.readlines()
              # print("Err File --------------{}-------------".format(proc_uid))
              # print(err_data)
              if (len(err_data) > 0):
                self.updt_proc_status(proc_uid, 'N/A', 'Failed')
              err_file.close()
          log_file.close()

        #   if len(log_file.readlines()) > 0:
        #     print(log_file.readlines().append(
        #       "{} successful".format(proc_uid)))
        #     if log_file.readlines()[-1:][0].__contains__("{} successful".format(proc_uid)):
        #       self.updt_proc_status(proc_uid, 99999, 'Successful')
        #   else:
        #     self.updt_proc_status(proc_uid, 99999, 'Running')
        # except Exception:
        #   traceback.print_exc()
        #   if len(err_file.readlines()) > 0:
        #     self.updt_proc_status(proc_uid, 99999, 'Failed')
    return 0

  def updt_proc_status(self, in_uid, in_pid, in_status):
    smo.SchedulerLoad.objects.filter(
      uid=in_uid).update(pid=in_pid, status=in_status)
    # smo_load['pid'] = in_pid
    # smo_load['status'] = in_status
    # smo_load.save()
    return

  def run_every_n_sec(self):
    sleep_sec = 60 / self.runs_per_min
    while(True):
      if self.run_end_typ == 'till-list-completes':
        self.get_process_status()
        if len(self.in_list) == 0 and len(self.all_active_proc) == 0:
          return 0
        else:
          print("Currently running {} {}".format(len(self.all_active_proc),
                "process" if len(self.all_active_proc) == 1 else "processes"))
          if self.limit_sessions == 0 or self.limit_sessions > len(self.all_active_proc):
            while(len(self.all_active_proc) - self.limit_sessions != 0 and len(self.in_list) > 0):
              print("Triggering new process")
              proc_data = self.in_list.pop(0)
              # print(proc_data)
              proc_uid = proc_data.split(' ')[1]
              out_file = '{}{}{}'.format(
                self.tempdir, os.path.sep, proc_uid)
              err_file = open('{}.err'.format(out_file), 'a')
              log_file = open('{}.log'.format(out_file), 'a')
              proc = po(proc_data, start_new_session=True,
                        shell=True, stdout=log_file, stderr=err_file)
              self.all_active_proc.append(proc)

              self.updt_proc_status(proc_uid, proc.pid, 'Started')
          else:
            print("Not triggering new process")
        sleep(sleep_sec)
      else:
        return

  def __init__(self, in_argv, in_run_end_typ, in_runs_per_min, in_data, in_type) -> None:
    # smo.SchedulerLoad.objects.all().delete()
    self.all_arg = in_argv
    print(self.all_arg)
    in_tmplt = json.loads(self.all_arg[2])
    self.tempdir = self.tempdir + os.path.sep + self.all_arg[1]
    if not os.path.exists(self.tempdir):
      os.mkdir(self.tempdir)
    print("Files generated at {}".format(self.tempdir))
    self.runs_per_min = in_runs_per_min
    self.run_end_typ = in_run_end_typ
    tmplt_vals = tmo.TemplateDef.objects.filter(
      id=in_tmplt["tmplt_id"]).values()
    # tmplt_vals = tmo.TemplateDef.objects.filter(
    #   vndr_nm='Oracle', prdct_typ='DB', prdct_nm='Oracle', prdct_ver='19', nm='timeout').values()
    if len(tmplt_vals) > 0:
      self.run_tmplt = Template(
        '{}\n--\n{}'.format(tmplt_vals[0]['text'], 'EXIT;'))
      for in_data_val in in_data:
        t = uuid.uuid4()
        # print(type(data))
        # sys.exit()
        val_context = {}
        if in_type == "csv":
          data = in_data_val.split(",")
          # print(data)
        if type(data) == str:
          val_context["var1"] = data
        elif type(data) == list:
          val_context = {"var{}".format(
            idx): data[idx].split("\n")[0] for idx in range(1, len(data))}
        # print(val_context)
        with open("{}{}{}.txt".format(self.tempdir, os.path.sep, t), "w") as file1:
          # Writing data to a file
          file1.writelines(self.run_tmplt.render(val_context))
          file1.close()
        curr_ts = datetime.now()
        smo_load = smo.SchedulerLoad(
          uid=t, prnt_uid=self.all_arg[1], file_pth="{}{}{}.txt".format(self.tempdir, os.path.sep, t), user_data=val_context, status="File created", crt_ts=curr_ts, updt_ts=curr_ts)
        smo_load.save()
        smo_config = smo.SchedulerConnectConfig.objects.filter(
          id=in_tmplt["cnnct_id"]).values()
        cnnct_cntxt = in_tmplt["cnnct_cntxt"]
        if len(smo_config) > 0:
          prerun_txt = 'cd {} &&'.format(
            smo_config[0]['cnnct_dir']) if smo_config[0]['cnnct_dir'] is not None else ''
          cnnct_cntxt['SCRPTFLPTH'] = "{}{}{}.txt".format(
            self.tempdir, os.path.sep, t)
          cnnct_txt = Template(
            smo_config[0]["cnnct_strng"]).render(cnnct_cntxt) + ' &&'
        else:
          prerun_txt = " "
          cnnct_txt = " "
        print("echo {} started && {} {} echo {} successful".format(
          t, prerun_txt, cnnct_txt, t))
        self.in_list.append("echo {} started && {} {} echo {} successful".format(
          t, prerun_txt, cnnct_txt, t))
      pass
    else:
      print('Template not found')


if __name__ == '__main__':
  # list_data = [
    # 'start "TEST{}" cmd /c "sleep 45 && echo Test{} >> test.txt"'.format(p, p) for p in range(0, 10)]
  # smo.SchedulerLoad.objects.all().delete()
  # print(sys.argv[0])
  # sys.exit()
  updt_process_status.upd_schedule(sys.argv[1], "Running")
  list_data = []
  for p in range(0, 10):
    sublist_data = []
    sublist_data.append("schema.index{}".format(p))
    sublist_data.append("schema.index{} part2".format(p))
    list_data.append(sublist_data)
    # list_data.append("schema.index{}".format(p))
  print(json.loads(sys.argv[2])["in_file"])
  # sys.exit(0)
  try:
    with open(json.loads(sys.argv[2])["in_file"], 'r') as in_file:
      list_data = in_file.readlines()
      in_file.close()
    rem = RunPerMin(sys.argv, 'till-list-completes', 10, list_data,
                    json.loads(sys.argv[2])["in_file"].split(".")[-1])
    # sys.exit()
    rem.run_every_n_sec()
    rem.get_process_status()
    updt_process_status.upd_schedule(sys.argv[1], "Completed")
  except:
    updt_process_status.upd_schedule(sys.argv[1], "Failed")
