from django.urls import path

from warehouse.views import *

app_name = 'warehouse'
urlpatterns = [
    path('<int:company_id>/products', WarehouseProductListCreateView.as_view()),
    path('<int:company_id>/products/<int:warehouse_product_id>', WarehouseProductRetrieveUpdateDeleteView.as_view()),
    path('<int:company_id>/summary', WarehouseSummaryView.as_view()),

]
