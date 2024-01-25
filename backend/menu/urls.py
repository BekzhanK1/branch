from django.urls import path, include

from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'menu', MenuItemViewSet, basename='menu')
router.register(r'categories', CategoryViewSet, basename='categories')

app_name = 'menu'
urlpatterns = [
    path('<int:company_id>/', include(router.urls)),
]