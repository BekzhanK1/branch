from django.urls import path, include

from company.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')

company_router = routers.DefaultRouter()
company_router.register(r'products', ProductViewSet, basename='products')
company_router.register(r'catalogs', CatalogViewSet, basename='catalogs')
company_router.register(r'employees', EmployeeViewSet, basename='employees')
company_router.register(r'orders', OrderViewSet, basename='orders')

app_name = 'company'
urlpatterns = [
    path('', include(router.urls)),
    path('company/<int:company_id>/', include(company_router.urls)),
]
