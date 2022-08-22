from django.urls import path
from . import views

urlpatterns = [path('', views.get_all_tmplts,
                    name='view_all_template'),
               path('create', views.create_template,
                    name='create_template'),
               path('list', views.get_all_tmplts,
                    name='view_all_template'),
               path('update/<int:id>', views.update_template,
                    name='update_template'),
               path('delete/<int:id>', views.delete_template,
                    name='delete_template'), ]
