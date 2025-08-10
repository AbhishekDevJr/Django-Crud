from rest_framework import serializers
from .models import Project, Task, ProjectFiles
from datetime import datetime

class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
        
    def get_created_by(self, instance):
        return instance.created_by.username if instance.created_by else ''
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ['created_by']
        
class ProjectListSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
        
    def get_created_by(self, instance):
        return instance.created_by.username if instance.created_by else ''
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'created_by', 'created_at']
        
class TaskSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        user = self.context['request'].user
        created_at = datetime.now()
        return Task.objects.create(**validated_data, assigned_to=user, created_at=created_at, project=validated_data["project"])
    
    def update(self, instance, validated_data):
        assigned_to = self.context["request"].user
        
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.status = validated_data.get("status", instance.status)
        
        if "project" in validated_data:
            project = validated_data.get("project", instance.project)
            instance.project = project
        
        instance.assigned_to = assigned_to
        instance.save()
        return instance
    
    class Meta:
        model = Task
        fields = ["title", "description", "project", "due_date", "status"]
        read_only_fields = ["created_at", "assigned_to"]
        
class TaskListSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    assigned_to = serializers.SerializerMethodField()
    
    def get_project(self, model_instance):
        return model_instance.project.title if model_instance.project else "N/A"
    
    def get_assigned_to(self, model_instance):
        return model_instance.assigned_to.username if model_instance.assigned_to else "N/A"
    
    class Meta:
        model = Task
        fields = "__all__"
        
        
class ProjectFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFiles
        fields = ['id', 'project', 'file', 'uploaded_at']