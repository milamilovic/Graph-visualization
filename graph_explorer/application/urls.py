from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('load_data_source', views.load_data_source, name='load_data_source'),
    path('search', views.search, name='search'),
    path('workspace', views.workspace, name='workspace'),
    path('load_workspace', views.load_workspace, name='load_workspace'),
    path('filter', views.filter_graph, name='filter'),
]