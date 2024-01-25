from django.urls import path, include

from warehouse.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'warehouse', WarehouseProductViewSet, basename='warehouse')

app_name = 'warehouse'
urlpatterns = [
    path('<int:company_id>/', include(router.urls)),
    path('<int:company_id>/warehouse/summary', WarehouseSummaryView.as_view()),

]
