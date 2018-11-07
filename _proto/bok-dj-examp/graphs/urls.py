from django.urls import include, path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('elements', views.elements, name='elements'),
    path('hexbin', views.hexbin, name='hexbin'),
    path('test', views.test, name='test'),
]
