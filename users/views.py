from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

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
            return Response({
                'status' : 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')            
            
            if not username or not password:
                return Response({
                    'status': 'error',
                    'message': 'Username & Password are required.'
                }, status=status.HTTP_400_BAD_REQUEST)
                 
            user = authenticate(username=username, password=password)
            
            if not user:
                return Response({
                    'status': 'success',
                    'message': 'Invalid Credentials'
                }, status=status.HTTP_200_OK)
                
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'status': 'success',
                'message': 'User Authenticated',
                'token': token.key
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
