from rest_framework import viewsets
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from rest_framework.decorators import api_view   
from rest_framework.response import Response
# it should be working, but it isn't
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# class MenuItemViewSet(viewsets.ModelViewSet):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

@api_view(['GET'])

def apiOverviewCategory(request): 
    api_urls = {
    'List':' /category-list/',
    'Detail View': ' /category-detail/<str:pk>/',
    'Create':' /category-create/',
    'Update': '/category-update',
    'Delete': '/category-delete'
    }
    return Response(api_urls)
def apiOverviewMenuItems(request): 
    api_urls = {
    'List':' /menu-items-list/',
    'Detail View': ' /menu-items-detail/<str:pk>/',
    'Create':' /menu-items-create/',
    'Update': '/menu-items-update',
    'Delete': '/menu-items-delete'
    }
    return Response(api_urls)

