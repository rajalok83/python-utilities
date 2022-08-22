from datetime import datetime
import json
import os
from tempfile import gettempdir
import traceback
import uuid
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from subprocess import Popen as po
import psutil
from . import models as smo
from . import updt_process_status
from . import scheduler_config
from django.views.decorators.csrf import csrf_exempt, csrf_protect


def schedule(request):
  # models.SchedulerProcess.objects.all().delete()
  if request.method == 'POST':
    uid = request.POST.get('uid')
    if uid is None:
      return HttpResponse("No UID was passed")
    else:
      schd_proc_mo = smo.SchedulerProcess.objects.filter(uid=t)
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
    vndr = request.GET.get('vndr')
    prdct_typ = request.GET.get('prdct_typ')
    prdct = request.GET.get('prdct')
    vrsn = request.GET.get('vrsn')
    dbid = request.GET.get('dbid')
    tag = request.GET.get('tag')
    # print(vrsn)
    t = uuid.uuid4()
    sub_txt = "Running"
    # smo.SchedulerProcess.objects.all().delete()
    # smo.SchedulerLoad.objects.all().delete()
    print("Count:" + str(smo.SchedulerProcess.objects.filter(tag=tag).count()))
    if smo.SchedulerProcess.objects.filter(tag=tag).count() == 0:
      sub_txt = "Started"
      print(sub_txt)
      if vndr is not None and nm is not None and tag is not None and prdct is not None and prdct_typ is not None and vrsn is not None and dbid is not None:
        tmplt_opt = {}
        tmplt_opt["vendor"] = vndr
        tmplt_opt["product_type"] = prdct_typ
        tmplt_opt["product"] = prdct
        tmplt_opt["version"] = vrsn
        tmplt_opt["template"] = nm
        tmplt_opt["tag"] = tag
        print(tmplt_opt)
      else:
        return HttpResponse("One of the required parameter(vndr, prdct_typ, prdct, vrsn, nm, tag) value is null")


#      proc = po("python ./scheduler/run_per_min.py {} {}".format(t, json.dumps(json.dumps(tmplt_opt))))
      print("{} ./scheduler/run_per_min.py {} {} {}".format((os.environ["VIRTUAL_ENV"] + '/Scripts/' if os.environ["VIRTUAL_ENV"] is not None else '') + 'python', t,
                                                            dbid, json.dumps(json.dumps(tmplt_opt))))
      proc = po("{} ./scheduler/run_per_min.py {} {} {}".format((os.environ["VIRTUAL_ENV"] + '/Scripts/' if os.environ["VIRTUAL_ENV"] is not None else '') + 'python', t,
                dbid, json.dumps(json.dumps(tmplt_opt))))
      scheduler_pid = proc.pid
      updt_process_status.add_schedule(scheduler_pid, t, tag, sub_txt)
    else:
      smp = smo.SchedulerProcess.objects.filter(tag=tag)[0]
      scheduler_pid = smp.pid
      t = smp.uid
      try:
        psutil.Process(scheduler_pid)
      except psutil.NoSuchProcess:
        sub_txt = "Completed"
        print(sub_txt)
    entry = {}
    entry["pid"] = t
    entry["status"] = sub_txt
    return render(request, "process.html", context=entry)
    # return HttpResponse("This process is scheduled with status {} with process id: {}".format(sub_txt, scheduler_pid))


def get_schedule(request, uid):
  sml = smo.SchedulerLoad.objects.filter(prnt_uid=uid).values()
  smp = smo.SchedulerProcess.objects.filter(uid=uid).values()
  out_load = {l["uid"]: l for l in sml}
  return render(request, "load.html", context={"list": out_load, "prnt_uid": uid, "status": smp[0]["status"] if len(smp) > 0 else "Not Found", "tag": smp[0]["tag"] if len(smp) > 0 else "Not Found"})
  # return HttpResponse("Schedule updated {}".format(uid))


def get_files(request, prnt_uid, flnm):
  with open('{}{}{}{}{}'.format(gettempdir(), os.path.sep, prnt_uid, os.path.sep, flnm), 'r') as fl:
    #   print('<br>'.join(fl.readlines()).replace('\\n', ''))
    fl.seek(0)
    return HttpResponse('<br>'.join(fl.readlines()).replace('\\n', ''))


def upd_schedule(request, uid, action):
  updt_process_status.upd_schedule(uid, action)
  return HttpResponse("Schedule updated {}:{}".format(uid, action))


@csrf_exempt
def create_connect_config(request):
  if request.method == "POST":
    try:
      in_body = json.loads(request.body.decode('utf-8'))
      print(in_body)
      t_def = scheduler_config.SchedulerConfiguration()
      t_def.create_scheduler_config(
        in_body["vndr_nm"], in_body["prdct_typ"], in_body["prdct_nm"], in_body["prdct_vrsn"], in_body["cnnct_dir"], in_body["cnnct_strng"])
      return HttpResponse("Create connect configuration successful!!!")
    except:
      traceback.print_exc()
      return HttpResponse("Create connect configuration failed!!!")
  else:
    return get_all_connect_config(request)


def get_all_connect_config(request):
  if request.method == "GET":
    all_config = smo.SchedulerConnectConfig.objects.all().values()
    # print(all_tmplt)
    out_load = {l["id"]: l for l in all_config}
    print(out_load)
    return render(request, "connect.html", context={"list": out_load})


@csrf_exempt
def delete_connect_config(request, id):
  if request.method == "POST":
    try:
      # print(id)
      smo.SchedulerConnectConfig.objects.get(id=id).delete()
      return HttpResponse("Delete connect config successful!!!")
    except:
      traceback.print_exc()
      return HttpResponse("Delete connect config failed!!!")
  else:
    return get_all_connect_config(request)


@csrf_exempt
def update_connect_config(request, id):
  if request.method == "POST":
    try:
      in_body = json.loads(request.body.decode('utf-8'))
      t_def = smo.SchedulerConnectConfig.objects.get(id=id)
      t_def.vndr_nm = in_body["vndr_nm"]
      t_def.prdct_typ = in_body["prdct_typ"]
      t_def.prdct_nm = in_body["prdct_nm"]
      t_def.prdct_ver = in_body["prdct_vrsn"]
      t_def.cnnct_dir = in_body["cnnct_dir"]
      t_def.cnnct_strng = in_body["cnnct_strng"]
      t_def.updt_ts = datetime.now()
      t_def.save()
      print()
      return HttpResponse("Update connect config successful!!!")
    except:
      traceback.print_exc()
      return HttpResponse("Update connect config failed!!!")
  else:
    return get_all_connect_config(request)
