from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . models import Project, Task
from . serializers import ProjectListSerializer, ProjectSerializer, TaskSerializer, TaskListSerializer, ProjectFilesSerializer

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
            
class ProjectUpdateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def patch(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    'status': 'error',
                    'message': 'Project ID is required!'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            project_obj = Project.objects.get(pk=pk)
            
            project_serialized = ProjectSerializer(project_obj, data=request.data, partial=True)
            
            if project_serialized.is_valid():
                project_serialized.save()
                return Response({
                    'status': 'success',
                    'message': f"Project with ID {pk} Updated.",
                    'data': ProjectSerializer(project_obj).data
                }, status=status.HTTP_200_OK)
            
        except Project.DoesNotExist as e:
            return Response({
                'status': 'error',
                'message': f'Project with ID {pk} does not exists',
                'exception': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Project.MultipleObjectsReturned as e:
            return Response({
                'status': 'error',
                'message': f'Multiple Projects found with ID {pk}',
                'exception': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                  
class ProjectDeleteView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def delete(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    'status': 'error',
                    'message': 'Project ID is required to perform Delete Action!'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            project_obj = Project.objects.get(pk=pk)            
            deleted_count, deleted_objs = project_obj.delete()
            
            return Response({
                'status': 'success',
                'message': f'Project with ID {pk} deleted.',
                'delete_count': deleted_count,
                'deleted_data': [str(deleted_objs.keys()) for item in deleted_objs.keys()]
            })
                
        except Project.DoesNotExist as e:
            return Response({
                'status': 'error',
                'message': f'Project with ID {pk} does not exist.',
                'exception': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Project.MultipleObjectsReturned as e:
            return Response({
                'status': 'error',
                'message': f'Multiple Projects found with ID {pk}.',
                'exception': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class TaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            if not request.data:
                return Response({
                    "status": "error",
                    "message": "Request Data is Invalid."
                }, status=status.HTTP_400_BAD_REQUEST)
                
            task_deserialized = TaskSerializer(data=request.data, context={"request": request})
            
            if task_deserialized.is_valid():
                task_obj = task_deserialized.save()
                return Response({
                    "status": "success",
                    "message": f"Task record created successfully with title: {task_obj.title}"
                }, status=status.HTTP_201_CREATED)
                
            return Response({
                "status": "error",
                "message": f"Request data is invalid",
                "data": request.data
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"{str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def get(self, request, pk):
        try:
            if not pk:
                return Response({
                    "status": "error",
                    "message": f"Task ID not found in the Request."
                }, status=status.HTTP_400_BAD_REQUEST)
                
            task_instance = Task.objects.get(id=pk)
            
            task_serialized = TaskListSerializer(task_instance, many=False)
            
            return Response({
                "status": "success",
                "message": f"Task data found for ID: {pk}",
                "data": task_serialized.data
            })
            
        except Task.DoesNotExist as e:
            return Response({
                "status": "error",
                "message": f"No Task data found for ID: {pk}.",
                "error_message": f"{str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Task.MultipleObjectsReturned as e:
            return Response({
                "status": "error",
                "message": f"Multiple Data found for single Task ID: {pk}",
                "error_message": f"{str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"{str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class TaskListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            task_qs = Task.objects.filter()
            
            if task_qs.exists():
                task_serialized = TaskListSerializer(task_qs, many=True)
                
                return Response({
                    "status": "success",
                    "message": f"Successfully fetched Task Data.",
                    "data": task_serialized.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "success",
                    "message": f"No Task data found."
                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"{str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class TaskUpdateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def patch(self, request, pk):
        try:
            if not pk:
                return Response({
                    "status": "error",
                    "message": f"Task ID is required for Task Update."
                }, status=status.HTTP_400_BAD_REQUEST)
                
            task_obj = Task.objects.get(pk=pk)
            task_serialized = TaskSerializer(task_obj, data=request.data, context={"request": request}, partial=True)
            
            if task_serialized.is_valid():
                task_saved_obj = task_serialized.save()
                
                return Response({
                    "status": "success",
                    "message": f"Task record updated with ID {pk}",
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": "error",
                "message": f"Error while updating Task Data with ID {pk}",
                "errors": task_serialized.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Task.MultipleObjectsReturned as e:
            return Response({
                "status": "error",
                "message": f"{str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Task.DoesNotExist as e:
            return Response({
                "status": "error",
                "message": f"{str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"{str(e)}"
            }, status=status.HTTP_501_NOT_IMPLEMENTED)
            
class ProjectFileUploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            project_file_serialized = ProjectFilesSerializer(data=request.data)
            
            if project_file_serialized.is_valid():
                project_file_serialized.save()
                return Response({
                    "status": "success",
                    "message": project_file_serialized.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "status": "error",
                "message": str(project_file_serialized.errors)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"{str(e)}"
            }, status=status.HTTP_501_NOT_IMPLEMENTED)