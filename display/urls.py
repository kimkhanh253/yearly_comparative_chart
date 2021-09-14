from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='search'),
    path(r'^form$', views.index, 'jtest.views.'),
    #path('<str:station1>/<str:station2>/<str:station3>/<str:year>',views.get_csv,name="download_csv"),

    
]