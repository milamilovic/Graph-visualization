from django.urls import path

from . import views
from .views import index

urlpatterns = [
    path('', views.index),
    path('load_data_source', views.load_data_source, name='load_data_source'),
    path('search', views.search, name='search'),
    path('filter', views.search, name='filter'),
]