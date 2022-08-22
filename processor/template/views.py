from datetime import datetime
import traceback
from django.shortcuts import render
from . import template_definition
# Create your views here.
from django.http import HttpResponse
from . import models as tmo
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json


@csrf_exempt
def delete_template(request, id):
  if request.method == "POST":
    try:
      tmo.TemplateDef.objects.get(id=id).delete()
      return HttpResponse("Delete template successful!!!")
    except:
      traceback.print_exc()
      return HttpResponse("Delete template failed!!!")
  else:
    return get_all_tmplts(request)


@csrf_exempt
def update_template(request, id):
  if request.method == "POST":
    try:
      in_body = json.loads(request.body.decode('utf-8'))
      t_def = tmo.TemplateDef.objects.get(id=id)
      t_def.nm = in_body["nm"]
      t_def.vndr_nm = in_body["vndr_nm"]
      t_def.prdct_typ = in_body["prdct_typ"]
      t_def.prdct_nm = in_body["prdct_nm"]
      t_def.prdct_ver = in_body["prdct_vrsn"]
      t_def.text = in_body["tmplt_txt"]
      t_def.updt_ts = datetime.now()
      t_def.save()
      return HttpResponse("Update template successful!!!")
    except:
      traceback.print_exc()
      return HttpResponse("Update template failed!!!")
  else:
    return get_all_tmplts(request)


def get_all_tmplts(request):
  if request.method == "GET":
    all_tmplt = tmo.TemplateDef.objects.all().values()
    # print(all_tmplt)
    out_load = {l["id"]: l for l in all_tmplt}
    # print(out_load)
    return render(request, "template.html", context={"list": out_load})


@csrf_exempt
def create_template(request):
  if request.method == "POST":
    try:
      in_body = json.loads(request.body.decode('utf-8'))
      print(in_body)
      t_def = template_definition.TemplateDefinition()
      t_def.create_template_def(
        in_body["vndr_nm"], in_body["prdct_typ"], in_body["prdct_nm"], in_body["prdct_vrsn"], in_body["nm"], in_body["tmplt_txt"])
      return HttpResponse("Create template successful!!!")
    except:
      traceback.print_exc()
      return HttpResponse("Create template failed!!!")
  else:
    return get_all_tmplts(request)

  # if request.method == "GET":
  #   nm = request.GET.get("nm")
  #   vndr = request.GET.get("vndr")
  #   prdct_typ = request.GET.get("prdct_typ")
  #   prdct = request.GET.get("prdct")
  #   vrsn = request.GET.get("vrsn")
  #   tmplt = request.GET.get("tmplt")
  #   if vndr is not None and nm is not None and prdct is not None and prdct_typ is not None and vrsn is not None and tmplt is not None:
  #     t_def = template_definition.TemplateDefinition()
  #     t_def.create_template_def(vndr, prdct_typ, prdct, vrsn,
  #                               nm, tmplt)
  #     return HttpResponse("Template creation successful")
  #   else:
  #     return HttpResponse("One of the required parameter(vndr, prdct_typ, prdct, vrsn, tmplt, nm) value is null")
  # else:
  #   return HttpResponse("Called with incorrect method")
