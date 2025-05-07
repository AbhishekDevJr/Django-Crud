from django.db import models
from . import Project
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=255, db_column='TASK TITLE')
    description = models.TextField(max_length=1000, null=True, blank=True, db_column='TASK DESCRIPTION')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task_project', db_column='RELATED PROJECT')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_user', db_column='RELATED USER')
    due_date = models.DateField(db_column='DUE DATE')
    status = models.CharField(choices={
        'Pending': 'Pending',
        'In Progress': 'In Progress',
        'Completed': 'Completed'
    }, db_column='STATUS')
    created_at = models.DateField(auto_now_add=True, db_column='CREATED AT')
    
    def __str__(self):
        return self.title