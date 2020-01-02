from django.urls import path

from . import views
from nmap_app.nmap_app import *

app_name = 'nmap_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('<server_ip>/', views.detail, name='detail'),
]

after_start()
