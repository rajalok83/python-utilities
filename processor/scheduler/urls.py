from django.urls import path
from . import views
app_name = "scheduler"
urlpatterns = [path('', views.schedule, name='scheduler'),
               path('upd/<str:uid>/<str:action>',
                    views.upd_schedule, name='scheduler'),
               ]
