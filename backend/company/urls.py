from django.urls import path, include

from company.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
router_product_catalog = routers.DefaultRouter()

router_product_catalog.register(r'products', ProductViewSet, basename='products')
router_product_catalog.register(r'catalogs', CatalogViewSet, basename='catalogs')


app_name = 'company'
urlpatterns = [
    path('', include(router.urls)),
    path('company/<int:company_id>/', include(router_product_catalog.urls)),
    
    # path('', CompanyListCreateView.as_view()),
    # path('<int:company_id>', CompanyRetrieveUpdateDeleteView.as_view()),
    
    # path('<int:company_id>/products', ProductListCreateView.as_view()),
    # path('<int:company_id>/products/<int:product_id>', ProductRetrieveUpdateDeleteView.as_view()),
    
    # path('<int:company_id>/catalogs', CatalogListCreateView.as_view()),
    # path('<int:company_id>/catalogs/<int:catalog_id>', CatalogRetrieveUpdateDeleteView.as_view()),

]
