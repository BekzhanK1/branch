from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import WarehouseProduct
from .serializers import WarehouseProductSerializer


class WarehouseProductListCreateView(APIView):
    def get(self, request, format=None):
        products = WarehouseProduct.objects.all()
        serializer = WarehouseProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WarehouseProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseSummaryView(APIView):
    def get(self, request, format=None):
        total_quantity = WarehouseProduct.objects.count()
        current_sum = WarehouseProduct.objects.filter(status=WarehouseProduct.Status.AVAILABLE).aggregate(models.Sum('total_price'))['total_price__sum']
        total_sum = WarehouseProduct.objects.aggregate(models.Sum('total_price'))['total_price__sum']

        return Response({
            'total_quantity': total_quantity,
            'current_sum': current_sum or 0,
            'total_sum': total_sum or 0,
        })
