#encoding: utf-8

from django.urls import path, include
from .views import v1,v2

app_name = 'api'

urlpatterns = [
    path('v1/client/', v1.ClientView.as_view(), name='v1_client'),
    path('v1/client/<ip>/', v1.ClientView.as_view(), name='v1_client_key'),
    path('v2/client/', v2.ClientView.as_view(), name='v2_client'),
    path('v2/client/<ip>/', v2.ClientView.as_view(), name='v2_client_key'),
]