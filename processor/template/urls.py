from django.urls import path
from . import views

urlpatterns = [path('', views.create_template_def,
                    name='create_template_definition')]
