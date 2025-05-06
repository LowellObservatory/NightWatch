from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hanisrad/',
         TemplateView.as_view(template_name="ldtplots/hanisrad.html"),
         name='hanisrad'),
    path('hanissat/',
         TemplateView.as_view(template_name="ldtplots/hanissat.html"),
         name='hanissat'),
    path('hanisboth/',
         TemplateView.as_view(template_name="ldtplots/hanisboth.html"),
         name='hanisboth'),
]
