from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_filters import rest_framework as filters
from django.db import models
from company.models import Company

from permissions import permission
from .models import WarehouseProduct
from .serializers import WarehouseProductSerializer


class WarehouseProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=WarehouseProduct.Status.choices)
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    price_per_unit = filters.RangeFilter()
    total_price = filters.RangeFilter()

    class Meta:
        model = WarehouseProduct
        fields = ['name', 'status', 'quantity', 'price_per_unit', 'total_price']
    


class WarehouseProductViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    serializer_class = WarehouseProductSerializer
    filterset_class = WarehouseProductFilter
    
    def get_queryset(self):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        
        if user.is_owner:
            company = get_object_or_404(Company, pk = company_id, company_owner = user)
            return WarehouseProduct.objects.filter(company = company)
        elif user.is_employee and company_id == user.company:
            return WarehouseProduct.objects.filter(company = user.company)
        else:
            PermissionDenied("You have no permission to access this company")


    def list(self, request, company_id=None):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
        page = request.GET.get('page')
        try:
            warehouse_products = paginator.page(page)
        except PageNotAnInteger:
            warehouse_products = paginator.page(1)
        except EmptyPage:
            warehouse_products = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(warehouse_products, many=True)
        return Response({
            'data': serializer.data,
            'pagination': {
                'page': warehouse_products.number,
                'pages': paginator.num_pages,
                'has_previous': warehouse_products.has_previous(),
                'has_next': warehouse_products.has_next(),
                'next_page': warehouse_products.next_page_number() if warehouse_products.has_next() else None,
                'previous_page': warehouse_products.previous_page_number() if warehouse_products.has_previous() else None,
                }
            })
    
    def create(self, request, company_id=None):
        user = request.user
        if user.is_owner:
            company = get_object_or_404(Company, company_owner = user, pk = company_id)
        if user.is_employee:
            company = user.company
        data = request.data
        data['company'] = company.pk
        data['receiver_staff'] = request.user.pk
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
    def retrieve(self,  request, pk = None, company_id=None):
        queryset = self.get_queryset()
        warehouseProduct = get_object_or_404(queryset, pk = pk)
        serializer = self.serializer_class(warehouseProduct)
        return Response(serializer.data)
    
    def partial_update(self, request, pk = None, company_id=None):
        queryset = self.get_queryset()
        warehouseProduct = get_object_or_404(queryset, pk = pk)
        serializer = self.serializer_class(warehouseProduct, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk = None, company_id=None):
        queryset = self.get_queryset()
        warehouseProduct = get_object_or_404(queryset, pk = pk)
        self.perform_destroy(warehouseProduct)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail = False, methods = ['get'])
    def summary(self, request, company_id = None):
        warehouse_products = self.get_queryset()
        total_quantity = warehouse_products.count()
        
        current_sum = warehouse_products.filter(
            status=WarehouseProduct.Status.AVAILABLE
        ).aggregate(models.Sum('total_price'))['total_price__sum']
        
        total_sum = warehouse_products.aggregate(models.Sum('total_price'))['total_price__sum']

        return Response({
            'total_quantity': total_quantity,
            'current_sum': current_sum or 0,
            'total_sum': total_sum or 0,
        })
        