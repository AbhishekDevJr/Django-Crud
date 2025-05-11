from django.urls import path
from . import views

urlpatterns = [
    path('project-list', views.ProjectListView.as_view(), name='project-list')
]