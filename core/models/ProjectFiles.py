from django.db import models
from . import Project

class ProjectFiles(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_files", db_column="PROJECT_FILES")
    file = models.FileField(upload_to="media/project_files")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.title} - {self.file.name}"