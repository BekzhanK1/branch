from django.urls import path

from warehouse.views import WarehouseProductListCreateView, WarehouseSummaryView

app_name = 'warehouse'
urlpatterns = [
    path('products/', WarehouseProductListCreateView.as_view(), name='warehouse-product-list-create'),
    path('summary/', WarehouseSummaryView.as_view(), name='warehouse-summary'),

]
