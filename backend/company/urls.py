from django.urls import path

from company.views import *

app_name = 'company'
urlpatterns = [
    path('', CompanyListCreateView.as_view()),
    path('<int:id>', CompanyRetrieveUpdateDeleteView.as_view()),
    path('products', ProductListCreateView.as_view()),
    path('products/<int:product_id>', ProductRetrieveUpdateDeleteView.as_view()),
    path('catalogs', CatalogListCreateView.as_view()),
    path('catalogs/<int:catalog_id>', CatalogRetrieveUpdateDeleteView.as_view()),

]
