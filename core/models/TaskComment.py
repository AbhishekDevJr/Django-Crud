from django.db import models
from . import Task
from django.contrib.auth.models import User

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comment', db_column='TASK')
    comment_text = models.TextField(max_length=1000, null=True, blank=True, default='Comment Not Added', db_column='COMMENT TEXT')
    commented_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='commented_user', db_column='COMMENTED BY')
    created_at = models.DateField(auto_now_add=True, db_column='CREATED AT')
    
    def __str__(self):
        return self.comment_text