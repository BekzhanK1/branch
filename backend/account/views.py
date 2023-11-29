import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import *
from utils import send_email



User = get_user_model()

# Create your views here.

def generate_password():
    return uuid.uuid4().hex[:10]

class EmployeeResetPasswordView(APIView):
    
    def post(self, request):
        
        user = request.user

        if user.is_superadmin or user.is_admin:
            data = request.data 

            if "email" not in data.keys():
                return Response({
                    "error": "'email' is required"
                }, status = status.HTTP_400_BAD_REQUEST)
            
            email = data['email']
            new_password = generate_password()
            
            user = User.objects.get(email = email)
            
            user.set_password(new_password)
            user.save()

            user_dict = UserSerializer(user).data
            user_dict['password'] = new_password

            send_email.send_credentials_to_employee(email, user.first_name, new_password, "reset_password_email.html")
            
            return Response({
                "status": "Password is changed successfully",
                "user": user_dict
            }, status = status.HTTP_200_OK)
        else:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )