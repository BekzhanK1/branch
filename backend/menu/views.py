from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from permissions import permission
from company.models import Company, CompanyEmployee



class MenuItemViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    serializer_class = MenuItemSerializer
    
    def get_queryset(self):
        user = self.request.user
        company_id = self.kwargs.get('company_id')

        if user.is_owner:
            company = get_object_or_404(Company, pk = company_id, company_owner = user)
            return MenuItem.objects.filter(company = company)
        elif user.is_employee and company_id == user.company:
            return MenuItem.objects.filter(company = user.company)
        else:
            PermissionDenied("You have no permission to access this company")
            
    def list(self, request, company_id=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, company_id = None):
        user = request.user
        if user.is_owner:
            company = get_object_or_404(Company, company_owner = user, pk = company_id)
        if user.is_employee:
            company = user.company
        data = request.data
        data['company'] = company.pk
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
    
    def retrieve(self,  request, pk = None, company_id=None):
        queryset = self.get_queryset()
        menuItem = get_object_or_404(queryset, pk = pk)
        serializer = self.serializer_class(menuItem)
        return Response(serializer.data)
    
    def partial_update(self, request, pk = None, company_id=None):
        queryset = self.get_queryset()
        menuItem = get_object_or_404(queryset, pk = pk)
        serializer = self.serializer_class(menuItem, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk = None, company_id=None):
        queryset = self.get_queryset()
        menuItem = get_object_or_404(queryset, pk = pk)
        self.perform_destroy(menuItem)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        user = self.request.user
        company_id = self.kwargs.get('company_id')

        if user.is_owner:
            company = get_object_or_404(Company, pk = company_id, company_owner = user)
            return Category.objects.filter(company = company)
        elif user.is_employee and company_id == user.company:
            return Category.objects.filter(company = user.company)
        else:
            PermissionDenied("You have no permission to access this company")
            
    def list(self, request, company_id=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, company_id = None):
        user = request.user
        if user.is_owner:
            company = get_object_or_404(Company, company_owner = user, pk = company_id)
        if user.is_employee:
            company = user.company
        data = request.data
        data['company'] = company.pk
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
    
    def retrieve(self,  request, pk = None, company_id=None):
        queryset = self.get_queryset()
        category = get_object_or_404(queryset, pk = pk)
        serializer = self.serializer_class(category)
        return Response(serializer.data)
    
    def partial_update(self, request, pk = None, company_id=None):
        queryset = self.get_queryset()
        category = get_object_or_404(queryset, pk = pk)
        serializer = self.serializer_class(category, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk = None, company_id=None):
        queryset = self.get_queryset()
        menuItem = get_object_or_404(queryset, pk = pk)
        self.perform_destroy(menuItem)
        return Response(status=status.HTTP_204_NO_CONTENT)
    