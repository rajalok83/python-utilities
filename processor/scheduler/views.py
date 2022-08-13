from datetime import datetime
import traceback
import uuid
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from subprocess import Popen as po
import psutil
from . import models
from . import updt_process_status


def schedule(request):
  # models.SchedulerProcess.objects.all().delete()
  if request.method == 'POST':
    uid = request.POST.get('uid')
    if uid is None:
      return HttpResponse("No UID was passed")
    else:
      schd_proc_mo = models.SchedulerProcess.objects.filter(uid=t)
      scheduler_pid = schd_proc_mo.pid
      sub_txt = "Running"
      try:
        psutil.Process(scheduler_pid)
      except psutil.NoSuchProcess:
        sub_txt = "Completed"
      updt_process_status.upd_schedule(uid, sub_txt)
      return HttpResponse("This is schedule App {} with process id: {}".format(sub_txt, scheduler_pid))
  elif request.method == 'GET':
    nm = request.GET.get('nm')
    t = uuid.uuid4()
    sub_txt = "Running"
    if models.SchedulerProcess.objects.filter(tag=nm).count() == 0:
      sub_txt = "Started"
      proc = po("python ./scheduler/run_per_min.py {}".format(t))
      scheduler_pid = proc.pid
      updt_process_status.add_schedule(scheduler_pid, t, nm, sub_txt)
    else:
      smp = models.SchedulerProcess.objects.filter(tag=nm)[0]
      scheduler_pid = smp.pid
      try:
        psutil.Process(scheduler_pid)
      except psutil.NoSuchProcess:
        sub_txt = "Completed"
    return HttpResponse("This is schedule App {} with process id: {}".format(sub_txt, scheduler_pid))


def upd_schedule(request, uid, action):
  updt_process_status.upd_schedule(uid, action)
  return HttpResponse("Schedule updated {}:{}".format(uid, action))
