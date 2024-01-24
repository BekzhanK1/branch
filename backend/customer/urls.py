from django.urls import include, path
from rest_framework import routers
from company.views import *
from .views import CustomerViewSet, AttendanceViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

app_name = 'customer'
urlpatterns = [
    path('', include(router.urls)),
]
