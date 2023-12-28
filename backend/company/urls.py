from django.urls import path

from company.views import *

app_name = 'company'
urlpatterns = [
    path('', CompanyListCreateView.as_view()),
    path('<int:company_id>', CompanyRetrieveUpdateDeleteView.as_view()),
    
    path('<int:company_id>/products', ProductListCreateView.as_view()),
    path('<int:company_id>/products/<int:product_id>', ProductRetrieveUpdateDeleteView.as_view()),
    
    path('<int:company_id>/catalogs', CatalogListCreateView.as_view()),
    path('<int:company_id>/catalogs/<int:catalog_id>', CatalogRetrieveUpdateDeleteView.as_view()),

]
