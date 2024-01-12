from django.urls import path

from .views import *

app_name = 'menu'
urlpatterns = [
    path('<int:company_id>/menu_items', MenuItemListCreateView.as_view()),
    path('<int:company_id>/menu_items/<int:menu_item_id>', MenuItemRetrieveUpdateDeleteView.as_view()),
    path('<int:company_id>/categories', CategoryListCreateView.as_view()),
    path('<int:company_id>/categories/<int:category_id>', CategorygRetrieveUpdateDeleteView.as_view()),
]