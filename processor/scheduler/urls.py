from django.urls import path
from . import views
app_name = "scheduler"
urlpatterns = [path('', views.schedule, name='scheduler'),
               path('upd/<str:uid>/<str:action>',
                    views.upd_schedule, name='scheduler'),
               path('schedule/<str:uid>',
                    views.get_schedule, name='scheduler'),
               path('load_files/<str:prnt_uid>/<str:flnm>',
                    views.get_files, name='scheduler'),
               path('connect_config',
                    views.get_all_connect_config, name='view_all_connect_config'),
               path('connect_config/list',
                    views.get_all_connect_config, name='view_all_connect_config'),
               path('connect_config/create',
                    views.create_connect_config, name='create_connect_config'),
               path('connect_config/update/<int:id>',
                    views.update_connect_config, name='update_connect_config'),
               path('connect_config/delete/<int:id>',
                    views.delete_connect_config, name='delete_connect_config'),
               ]
