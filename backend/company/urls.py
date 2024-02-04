from django.urls import path, include

from company.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')

company_router = routers.DefaultRouter()
company_router.register(r'product', ProductViewSet, basename='product')
company_router.register(r'catalog', CatalogViewSet, basename='catalog')
company_router.register(r'employee', EmployeeViewSet, basename='employee')
company_router.register(r'order', OrderViewSet, basename='orders')
company_router.register(r'position', EmployeePositionViewSet, basename='position')

app_name = 'company'
urlpatterns = [
    path('', include(router.urls)),
    path('company/<int:company_id>/', include(company_router.urls)),
]
