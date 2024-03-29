from django.urls import path
from . import views
app_name = "scheduler"
urlpatterns = [
  # path('', views.schedule, name='scheduler'),
  path('run', views.schedule, name='scheduler'),
  path('upd/<str:uid>/<str:action>',
       views.upd_schedule, name='upd_schedule'),
  path('execution/<str:uid>',
       views.get_execution, name='get_execution'),
  path('execution/delete/<str:uid>',
       views.delete_execution, name='delete_execution'),
  path('executions',
       views.get_all_executions, name='get_all_executions'),
  path('load_files/<str:prnt_uid>/<str:flnm>',
       views.get_files, name='scheduler'),
  path('connect_config',
       views.get_all_connect_config, name='view_all_connect_config'),
  path('connect_config/get',
       views.get_connect_config, name='get_connect_config'),
  path('connect_config/get/<int:id>',
       views.get_connect_config_by_id, name='get_connect_config_by_id'),
  path('connect_config/list',
       views.get_all_connect_config, name='view_all_connect_config'),
  path('connect_config/create',
       views.create_connect_config, name='create_connect_config'),
  path('connect_config/update/<int:id>',
       views.update_connect_config, name='update_connect_config'),
  path('connect_config/delete/<int:id>',
       views.delete_connect_config, name='delete_connect_config'),
]
