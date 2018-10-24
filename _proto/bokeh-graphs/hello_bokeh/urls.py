from django.contrib import admin
from django.urls import include, path

from graphs import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('graphs/', include('graphs.urls'))
]
