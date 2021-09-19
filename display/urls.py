from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='search'),
    #path(r'^form$', views.index, 'jtest.views.'),
    
]