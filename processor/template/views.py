from django.shortcuts import render
from . import template_definition
# Create your views here.
from django.http import HttpResponse


def create_template_def(request):
  t_def = template_definition.TemplateDefinition()
  t_def.create_template_def('Oracle', 'DB', 'Oracle', '19',
                            'timeout', 'timeout 15')
  return HttpResponse("Template creation succesful")
