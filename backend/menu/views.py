from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from .permissions import *
























# from rest_framework import viewsets
# from .models import Category, MenuItem
# from .serializers import CategorySerializer, MenuItemSerializer
# from rest_framework.decorators import api_view   
# from rest_framework.response import Response
# # it should be working, but it isn't
# # class CategoryViewSet(viewsets.ModelViewSet):
# #     queryset = Category.objects.all()
# #     serializer_class = CategorySerializer

# # class MenuItemViewSet(viewsets.ModelViewSet):
# #     queryset = MenuItem.objects.all()
# #     serializer_class = MenuItemSerializer

# @api_view(['GET'])
# def apiOverviewCategory(request): 
#     api_urls = {
#     'List':' /category-list/',
#     'Detail View': ' /category-detail/<str:pk>/',
#     'Create':' /category-create/',
#     'Update': '/category-update',
#     'Delete': '/category-delete'
#     }
#     return Response(api_urls)
# def apiOverviewMenuItems(request): 
#     api_urls = {
#     'List':' /menu-items-list/',
#     'Detail View': ' /menu-items-detail/<str:pk>/',
#     'Create':' /menu-items-create/',
#     'Update': '/menu-items-update',
#     'Delete': '/menu-items-delete'
#     }
#     return Response(api_urls)

# @api_view(['GET'])
# def categoryList(request):
#     queryset = Category.objects.all()
#     serializer = CategorySerializer(queryset, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def menuItemList(request):
#     queryset = MenuItem.objects.all()
#     serializer = MenuItemSerializer(queryset, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def categoryDetail(request, pk):
#     queryset = Category.objects.get(id=pk)
#     serializer = CategorySerializer(queryset, many = False)
#     return Response(serializer.data)

# @api_view(['GET'])
# def menuItemDetail(request, pk):
#     queryset = MenuItem.objects.get(id=pk)
#     serializer = MenuItemSerializer(queryset, many = False)
#     return Response(serializer.data)

# @api_view(['POST'])
# def categoryCreate(request):
#     serializer = CategorySerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['POST'])
# def menuItemCreate(request):
#     serializer = MenuItemSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['POST'])
# def categoryUpdate(request,pk):
#     queryset = Category.objects.get(id=pk)
#     serializer = CategorySerializer(instance= queryset,data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['POST'])
# def menuItemUpdate(request,pk):
#     queryset = MenuItem.objects.get(id=pk)
#     serializer = MenuItemSerializer(instance=queryset,data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def categoryDelete(request, pk):
#     queryset = Category.objects.get(id=pk)
#     queryset.delete()
#     return Response("Item successfully deleted")

# @api_view(['DELETE'])
# def menuItemDelete(request, pk):
#     queryset = MenuItem.objects.get(id=pk)
#     queryset.delete()
#     return Response("Item successfully deleted")
