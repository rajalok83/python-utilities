from datetime import datetime
from django.db import models

# Create your models here.


class SchedulerConnectConfig(models.Model):
  class Meta:
    unique_together = (('vndr_nm', 'prdct_typ', 'prdct_nm', 'prdct_ver'))
  vndr_nm = models.CharField(max_length=30)
  prdct_typ = models.CharField(max_length=30)
  prdct_nm = models.CharField(max_length=30)
  prdct_ver = models.CharField(max_length=30)
  cnnct_dir = models.CharField(max_length=3200)
  cnnct_strng = models.CharField(max_length=3200)
  crt_ts = models.DateTimeField('date created', default=datetime.now())
  updt_ts = models.DateTimeField('date updated', default=datetime.now())


class SchedulerProcess(models.Model):
  pid = models.BigIntegerField(unique=True)
  uid = models.CharField(max_length=80, primary_key=True)
  cnnct_id = models.BigIntegerField(default=-9999)
  tmplt_id = models.BigIntegerField(default=-9999)
  tag = models.CharField(max_length=80, unique=True, default='')
  cnnct_cntxt = models.CharField(max_length=32000, default='')
  status = models.CharField(max_length=80, default='')
  crt_ts = models.DateTimeField('date created', default=datetime.now())
  updt_ts = models.DateTimeField('date updated', default=datetime.now())

  def __str__(self) -> str:
    return super().__str__()


class DBTyp(models.Model):
  nm = models.CharField(max_length=30, primary_key=True)

  def __str__(self) -> str:
    return "{ 'nm': '{}' }".format(self.nm)


class SchedulerLoad(models.Model):
  uid = models.CharField(max_length=80, unique=True)
  prnt_uid = models.CharField(max_length=80)
  pid = models.CharField(default="", max_length=10)
  user_data = models.CharField(default='', max_length=3200)
  prirty = models.BigIntegerField(default=-9999)
  file_pth = models.CharField(max_length=3200)
  status = models.CharField(max_length=80)
  crt_ts = models.DateTimeField('date created')
  updt_ts = models.DateTimeField('date updated')

  def __str__(self) -> str:
    return super().__str__()


class ScheduleConfig(models.Model):
  class Meta:
    unique_together = (('typ', 'nm'))

  typ = models.ForeignKey(DBTyp, on_delete=models.CASCADE)
  nm = models.CharField(max_length=80)
  val = models.CharField(max_length=3200)
  crt_ts = models.DateTimeField('date created')
  updt_ts = models.DateTimeField('date updated')

  def __str__(self) -> str:
    return "{ 'typ': '{}', 'nm': '{}', 'val': '{}', 'crt_ts': '{}', 'updt_ts': '{}' }".format(self.typ, self.nm, self.val, self.crt_ts, self.updt_ts)
