from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers

# from warehouse.views import WarehouseProductListCreateView, WarehouseSummaryView
from .views import *
from account import views as account_views


urlpatterns = [
    path('login', LoginView.as_view()),
    path('register-owner', OwnerRegistrationView.as_view()),
    path('register-employee', EmployeeRegistrationView.as_view()),
    path('register-customer', CustomerRegistrationView.as_view()),
    path('activate/<uidb64>/<token>', ActivateClass.as_view(), name="activate"),

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    path('reset-password', account_views.EmployeeResetPasswordView.as_view()),
    path('reset-password-admin', account_views.AdminResetPasswordView.as_view()),
    path('reset/<uidb64>/<token>', SetNewPasswordAdmin.as_view(), name="reset"),

    path('warehouse/', include('warehouse.urls')),
    path('company/', include('company.urls')),
    path('menu/', include('menu.urls')),
    path('', include('customer.urls')),
    
]
