# synapse_api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/data/', views.get_data, name='get_data'),
    path('api/filterdata/', views.filter_data, name='filter_data'),
]
