from django.shortcuts import render
import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import *
from utils import generate_password



User = get_user_model()

# Create your views here.
class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        
        user = request.user
        if not user.is_superadmin or not user.is_admin:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data 

        if "user_id" not in data.keys():
            return Response({
                "error": "'user_id' is required"
            }, status = status.HTTP_400_BAD_REQUEST)
        
        user_id = data['user_id']
        new_password = generate_password()
        
        user = User.objects.get(pk = int(user_id))
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            "status": "Password is changed successfully",
            "user": UserSerializer(user).data
        }, status = status.HTTP_200_OK)