from django.db import models

# Create your models here.


class TemplateDef(models.Model):
  class Meta:
    unique_together = (('vndr_nm', 'prdct_typ', 'prdct_nm', 'prdct_ver', 'nm'))
  vndr_nm = models.CharField(max_length=30)
  prdct_typ = models.CharField(max_length=30)
  prdct_nm = models.CharField(max_length=30)
  prdct_ver = models.CharField(max_length=30)
  nm = models.CharField(max_length=80)
  text = models.CharField(max_length=3200)
  crt_ts = models.DateTimeField('date created')
  updt_ts = models.DateTimeField('date updated')
