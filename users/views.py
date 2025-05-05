from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer

class RegistrationView(APIView):
    permission_classes=[]
    authentication_classes=[]
    
    def post(self, request):
        
        try:    
            serializer = UserRegistrationSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'User Registered Successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'error',
                    'message': 'User Data is not Valid.',
                    'data': request.data
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            Response({
                'status' : 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
