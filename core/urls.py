from django.urls import path
from . import views

urlpatterns = [
    path('project-list', views.ProjectListView.as_view(), name='project-list'),
    path('project-list/<int:pk>', views.ProjectView.as_view(), name='project-list-id'),
    path('project-list/create-new', views.ProjectView.as_view(), name='project-list-create-new'),
    path('project/update/<int:pk>', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/delete/<int:pk>', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('task/create-new', views.TaskView.as_view(), name="task-create-new"),
    path('task/list-view', views.TaskListView.as_view(), name="task-list-view"),
    path('task/list-view/<int:pk>', views.TaskView.as_view(), name="task-detail-view"),
    path('task/update/<int:pk>', views.TaskUpdateView.as_view(), name='task-udpate'),
    path('project-file-upload', views.ProjectFileUploadView.as_view(), name='project-file-upload')
]