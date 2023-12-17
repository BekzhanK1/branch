from django.urls import path

from company.views import CompanyListCreateView, CompanyRetrieveUpdateDeleteView, ProductListCreateView, ProductRetrieveUpdateDeleteView

app_name = 'company'
urlpatterns = [
    path('', CompanyListCreateView.as_view()),
    path('<int:id>', CompanyRetrieveUpdateDeleteView.as_view()),
    path('<int:company_id>/products', ProductListCreateView.as_view()),
    path('<int:company_id>/products/<int:product_id>', ProductRetrieveUpdateDeleteView.as_view()),

]
