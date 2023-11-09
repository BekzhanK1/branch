from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

from account.serializers import UserSerializer


# Create your views here.

class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
        
    def post(self, request):
        
        data = request.data
        
        if "email" not in data.keys():
            return Response({
                "error": "Email is required"
            }, status= status.HTTP_400_BAD_REQUEST)
            
        if "password" not in data.keys():
            return Response({
                "error": "Password is required"
            }, status= status.HTTP_400_BAD_REQUEST)
            
        email = data['email']
        password = data['password']
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            user_id = User.objects.get(email=email)
            data = self.get_tokens_for_user(user_id)
            return Response(data, status = status.HTTP_200_OK)
        else:
            return Response({
                "error": "User does not exist"
            }, status= status.HTTP_400_BAD_REQUEST)
            