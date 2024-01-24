import uuid
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from api.tokens import account_token

from account.serializers import *
from company.models import CompanyEmployee, Company
from utils import send_email

from .tasks import send_credentials_to_employee, activateEmail

User = get_user_model()


from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode

from myproject.settings import SITE_URL

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

        except:
            user = None

        if user is not None and account_token.check_token(user, token):
            user.is_active = True
            user.save()

            # messages.success(
            #     request, "Thank you for your email confirmation. Now you can login your account.")
            return Response({"success": "successfully activated account"}, status=status.HTTP_200_OK)
        # else:
        #     messages.error(request, "Activation link is invalid!")

        return Response({"error": "couldn't activate account"}, status=status.HTTP_400_BAD_REQUEST)


class AdminRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def send_activation_email(self, request, user: User):
        
        activation_dict = {
            'user': user.first_name + " " + user.last_name,
            'domain_name': SITE_URL,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http',
            'to_email': user.email,
            'template': 'template_activate_account.html'
        }
        
        print(activation_dict)
        activateEmail.delay(**activation_dict)
        

    def post(self, request):

        # user = request.user

        # if not user.is_superadmin:
        #     return Response(
        #         {'error': "You don't have a permission"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # user.save()
            data = get_tokens_for_user(user)
            
            # print(data)
            # send_email.activateEmail(request, user, user.email)
            # activateEmail.delay(user, user.email)
            self.send_activation_email(request, user)
            
            response_dict = {'user': UserSerializer(user).data}
            response_dict.update(data)
            return Response(data, status=status.HTTP_201_CREATED)

        # Creating dict with errors, keys are field names, values are error messages
        errors = {}
        for field, error_detail in serializer.errors.items():
            errors[field] = error_detail[0]

        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)


def generate_password():
    return uuid.uuid4().hex[:10]


class EmployeeRegistrationView(APIView):
    # permission_classes = (permissions.AllowAny,)

    def post(self, request):

        user = request.user
        # if not user.is_superadmin or not user.is_admin:
        # if not user.is_superadmin or not user.is_admin:
        #     return Response(
        #         {'error': "You don't have a permission"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        if user.is_superadmin or user.is_admin:
            password_generated = generate_password()
            # print(password_generated)
            request.data['password'] = password_generated
            
            if not "company_id" in request.data:
                    return Response({
                        "error": "Company_id field is required"
                    }, status = status.HTTP_400_BAD_REQUEST)
                    
            company_id = request.data.pop("company_id")

            serializer = EmployeeRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                data = get_tokens_for_user(user, password_generated)
                
                admin_user = request.user
                
                # Creating new CompanyEmployee and assign the data
                # company = get_object_or_404(Company, company_owner=admin_user)
                
                if not Company.objects.filter(pk = int(company_id), company_owner = admin_user).exists():
                    return Response({
                        "error": "Company does not exist"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                company = Company.objects.get(pk = int(company_id), company_owner = admin_user)
                
                company_employee_data = {'company': company, 'employee': user, 'title': 'Employee'}
                CompanyEmployee.objects.create(**company_employee_data)

                # send_email.send_credentials_to_employee(user.email, user.first_name, password_generated,
                #                                         "registration_email.html")
                
                send_credentials_to_employee.delay(user.email, user.first_name, password_generated,
                                                        "registration_email.html")
                
                response_dict = {'user': UserSerializer(user)}
                response_dict.update(data)
                return Response(data, status=status.HTTP_201_CREATED)

            # Creating dict with errors, keys are field names, values are error messages
            errors = {}
            for field, error_detail in serializer.errors.items():
                errors[field] = error_detail[0]

            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )


class SetNewPasswordAdmin(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uidb64, token):
        User = get_user_model()
        data = request.data
        if "password" not in data.keys():
            return Response({"error": "Password is required"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            # print(user)


        except:
            user = None

        if user is not None and account_token.check_token(user, token):
            user.set_password(data["password"])
            user.save()
            # print(user.password)


            # messages.success(
            #     request, "Thank you for your email confirmation. Now you can login your account.")
            return Response({"success": "successfully changed password"}, status=status.HTTP_200_OK)
        # else:
        #     messages.error(request, "Activation link is invalid!")
        return Response({"error": "couldn't change password"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def send_activation_email(self, request, user: User):
        
        activation_dict = {
            'user': user.first_name + " " + user.last_name,
            'domain_name': SITE_URL,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http',
            'to_email': user.email,
            'template': 'template_activate_account.html'
        }
        
        print(activation_dict)
        activateEmail.delay(**activation_dict)
        

    def post(self, request):


        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # user.save()
            data = get_tokens_for_user(user)
            
            self.send_activation_email(request, user)
            
            response_dict = {'user': UserSerializer(user).data}
            response_dict.update(data)
            return Response(data, status=status.HTTP_201_CREATED)

        # Creating dict with errors, keys are field names, values are error messages
        errors = {}
        for field, error_detail in serializer.errors.items():
            errors[field] = error_detail[0]

        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)

