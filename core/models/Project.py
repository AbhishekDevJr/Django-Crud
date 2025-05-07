from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=255, db_column='PROJECT TITLE')
    description = models.TextField(max_length=1000, null=True, blank=True, db_column='PROJECT DESCRIPTION')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_created_by', db_column='CREATED BY')
    created_at = models.DateField(auto_now_add=True, db_column='CREATED AT')
    
    def __str__(self):
        return self.title
    