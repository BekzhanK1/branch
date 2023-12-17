from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import WarehouseProduct
from .serializers import WarehouseProductSerializer


class WarehouseProductListCreateView(APIView):
    def get(self, request, company_id):
        products = WarehouseProduct.objects.filter(company=company_id)
        serializer = WarehouseProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, company_id):
        request.data['company'] = company_id
        serializer = WarehouseProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseProductRetrieveUpdateDeleteView(APIView):
    def get(self, request, company_id, warehouse_product_id):
        try:
            warehouse_product = WarehouseProduct.objects.get(company=company_id, pk=warehouse_product_id)
            serializer = WarehouseProductSerializer(warehouse_product)
            return Response(serializer.data)
        except:
            return Response({"error": "WarehouseProduct not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, company_id, warehouse_product_id):
        warehouse_product = WarehouseProduct.objects.get(company=company_id, pk=warehouse_product_id)
        serializer = WarehouseProductSerializer(warehouse_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, warehouse_product_id):
        warehouse_product = WarehouseProduct.objects.get(company=company_id, pk=warehouse_product_id)
        warehouse_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WarehouseSummaryView(APIView):
    def get(self, request, company_id, format=None):
        total_quantity = WarehouseProduct.objects.filter(company=company_id).count()
        current_sum = WarehouseProduct.objects.filter(
            company=company_id, status=WarehouseProduct.Status.AVAILABLE
        ).aggregate(models.Sum('total_price'))['total_price__sum']
        total_sum = WarehouseProduct.objects.filter(company=company_id).aggregate(models.Sum('total_price'))['total_price__sum']

        return Response({
            'total_quantity': total_quantity,
            'current_sum': current_sum or 0,
            'total_sum': total_sum or 0,
        })