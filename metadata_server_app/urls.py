from django.urls import path
from . import views
from . import plugins

urlpatterns = [
    path('', views.list_metadata, name='list-metadata'),
    path('download_readme/<int:metadata_id>/', plugins.download_readme, name='download_readme'),
    path('insert-metadata/', views.insert_metadata, name='insert-metadata')
]