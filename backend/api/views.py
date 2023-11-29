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
from .tokens import account_activation_token
from utils import generate_password

User = get_user_model()


# Create your views here.

def get_tokens_for_user(user, password=None):
    refresh = RefreshToken.for_user(user)

    user = UserSerializer(user).data
    if password is not None:
        user['password'] = password

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': user
    }


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        data = request.data

        if "email" not in data.keys():
            return Response({
                "error": "Email is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        if "password" not in data.keys():
            return Response({
                "error": "Password is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        email = data['email']
        password = data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user_id = User.objects.get(email=email)
            data = get_tokens_for_user(user_id)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "User does not exist or activation required"
            }, status=status.HTTP_400_BAD_REQUEST)


class ActivateClass(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            print('Here')

        except:
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            # messages.success(
            #     request, "Thank you for your email confirmation. Now you can login your account.")
            return Response({"success": "successfully activated account"}, status=status.HTTP_200_OK)
        # else:
        #     messages.error(request, "Activation link is invalid!")

        return Response({"error": "couldn't activate account"}, status=status.HTTP_400_BAD_REQUEST)


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.first_name + " " + user.last_name,
        'domain': "localhost:8000",
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        return Response({"success": f"successfully sent email to {to_email}"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": f"problem sending email to {to_email}"}, status=status.HTTP_400_BAD_REQUEST)


class AdminRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        user = request.user

        if not user.is_superadmin:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            activateEmail(request, user, user.email)
            data = get_tokens_for_user(user)
            response_dict = {'user': UserSerializer(user)}
            response_dict.update(data)
            return Response(data, status=status.HTTP_201_CREATED)

        # Creating dict with errors, keys are field names, values are error messages
        errors = {}
        for field, error_detail in serializer.errors.items():
            errors[field] = error_detail[0]

        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)


def send_credentials_to_employee(user_email, first_name, password):
    template = get_template('registration_email.html')

    context = {
        'first_name': first_name,
        'password': password,
    }
    html_content = template.render(context)

    email = EmailMessage(
        "brunch.kz registration complete",
        html_content,
        to=[user_email]
    )
    email.content_subtype = "html"
    email.send()


class EmployeeRegistrationView(APIView):
    # permission_classes = (permissions.AllowAny,)

    def post(self, request):

        user = request.user
        if not user.is_superadmin or not user.is_admin:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )

        password_generated = generate_password()
        request.data['password'] = password_generated

        serializer = EmployeeRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = get_tokens_for_user(user, password_generated)

            send_credentials_to_employee(user.email, user.first_name, password_generated)
            response_dict = {'user': UserSerializer(user)}
            response_dict.update(data)
            return Response(data, status=status.HTTP_201_CREATED)

        # Creating dict with errors, keys are field names, values are error messages
        errors = {}
        for field, error_detail in serializer.errors.items():
            errors[field] = error_detail[0]

        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
    
