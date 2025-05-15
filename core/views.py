from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . models import Project
from . serializers import ProjectListSerializer, ProjectSerializer

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
            
class ProjectView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    'status': 'error',
                    'message': 'Project ID is Required to fetch Specific Project Data'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            project_obj = Project.objects.get(pk=pk)
            project_serialized = ProjectSerializer(project_obj).data
            
            return Response({
                'status': 'success',
                'message': f'Project Data Found for ID: {pk}',
                'data': project_serialized 
            }, status=status.HTTP_200_OK)
            
        except Project.DoesNotExist:
            return Response({
                'status': 'error',
                'message': f'No Project found for specified ID: {pk}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Project.MultipleObjectsReturned:
            return Response({
                'status': 'error',
                'message': f'Multiple Projects found for specified ID: {pk}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def post(self, request):
        try:
            if not request.data:
                return Response({
                    'status': 'error',
                    'message': 'Request Payload is Invalid',
                    'data': request.data
                }, status=status.HTTP_400_BAD_REQUEST)
                
            project_deserialized = ProjectSerializer(data=request.data, context={'request': request})
            
            if project_deserialized.is_valid():
                project_obj = project_deserialized.save()
                return Response({
                    'status': 'success',
                    'message': 'Project Record created successfully',
                    'data': project_obj.title
                }, status=status.HTTP_201_CREATED)
                
            return Response({
                'status': 'error',
                'message': 'Request Payload is Invalid',
                'data': request.data
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)