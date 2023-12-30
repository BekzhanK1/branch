import uuid

from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import *
from utils import send_email

User = get_user_model()

from api.tokens import account_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode

from api.tasks import send_reset_password_email_to_admin

from myproject.settings import SITE_URL

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
                }, status=status.HTTP_400_BAD_REQUEST)

            email = data['email']
            new_password = generate_password()

            user = User.objects.get(email=email)

            user.set_password(new_password)
            user.save()

            user_dict = UserSerializer(user).data
            user_dict['password'] = new_password

            send_email.send_credentials_to_employee(email, user.first_name, new_password, "reset_password_email.html")

            return Response({
                "status": "Password is changed successfully",
                "user": user_dict
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )


class AdminResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def send_reset_password_to_admin(self, request, user, email):
        
        request_dict = {
            'admin': user.first_name + " " + user.last_name,
            'domain': SITE_URL,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http',
            'to_email': email
        }
        
        send_reset_password_email_to_admin.delay(**request_dict)

    def post(self, request):
        data = request.data
        if "email" not in data.keys():
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        email = data["email"]

        try:
            user = User.objects.get(email=email)
        except:
            return Response({"error": "User with this email doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_admin:
            return Response({"error": "User with this email doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        # send_email.send_reset_password_email_to_admin(request, user, email)
        
        self.send_reset_password_to_admin(request, user, email)
        
        return Response({"message": f"Email sent to {email}"})
