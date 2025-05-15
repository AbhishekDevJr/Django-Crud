from rest_framework import serializers
from .models import Project

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