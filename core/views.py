from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . models import Project
from . serializers import ProjectListSerializer

class ProjectListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            project_data = Project.objects.all()
            
            if not project_data:
                return Response({
                    'status': 'success',
                    'message': 'Project data not found',
                    'data': []
                }, status=status.HTTP_200_OK)
                
            serialized_data = ProjectListSerializer(project_data, many=True)
            return Response({
                'status': 'success',
                'message': 'Project Data Found',
                'data': serialized_data.data
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)