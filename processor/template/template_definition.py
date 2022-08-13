import django
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'processor.settings'
django.setup()
from datetime import date, datetime
from template import models as tmo


class TemplateDefinition:
  def get_template_def(self) -> str:
    return None

  def create_template_def(self, in_vndr_nm, in_prdct_typ, in_prdct_nm, in_prdct_ver, in_nm, in_text) -> bool:
    curr_ts = datetime.now()
    t = tmo.TemplateDef(
      vndr_nm=in_vndr_nm,
      prdct_typ=in_prdct_typ,
      prdct_nm=in_prdct_nm,
      prdct_ver=in_prdct_ver,
      nm=in_nm,
      text=in_text,
      crt_ts=curr_ts,
      updt_ts=curr_ts)
    t.save()
    return True

  def __str__(self) -> str:
    pass

  def __init__(self) -> None:
    pass


if __name__ == '__main__':
  t_def = TemplateDefinition()
  t_def.create_template_def('Oracle', 'DB', 'Oracle', '19',
                            'rebuild_index_offline', 'REBUILD INDEX {{ var0 }} OFFLINE;')
