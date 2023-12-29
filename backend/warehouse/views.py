from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from company.models import Company, CompanyEmployee

from company.permissions import AdminLevelPermission, EmployeeLevelPermission
from .models import WarehouseProduct
from .serializers import WarehouseProductSerializer


class WarehouseProductListCreateView(APIView):
    permission_classes = (EmployeeLevelPermission, )
    def get(self, request, company_id):
        user = request.user
        
        company = Company.objects.get(pk = int(company_id))
        
        if user.is_admin and (company.company_owner.id != user.id):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        elif user.is_employee and not (CompanyEmployee.objects.filter(companyid = int(company_id), employeeid = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)

        products = WarehouseProduct.objects.filter(company=company)
        serializer = WarehouseProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, company_id):
        user = request.user
        
        company = Company.objects.get(pk = int(company_id))
        
        if user.is_admin and (company.company_owner.id != user.id):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        elif user.is_employee and not (CompanyEmployee.objects.filter(companyid = int(company_id), employeeid = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
            
        request.data['company'] = company_id
        serializer = WarehouseProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseProductRetrieveUpdateDeleteView(APIView):
    def get(self, request, company_id, warehouse_product_id):
        user = request.user
        
        company = Company.objects.get(pk = int(company_id))
        if user.is_admin and (company.company_owner.id != user.id):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        elif user.is_employee and not (CompanyEmployee.objects.filter(companyid = int(company_id), employeeid = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        if not WarehouseProduct.objects.filter(pk = warehouse_product_id).exists():
            return Response({
            "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)
            
        warehouse_product = WarehouseProduct.objects.get(company=company_id, pk=warehouse_product_id)
        serializer = WarehouseProductSerializer(warehouse_product)
        return Response(serializer.data)

    def patch(self, request, company_id, warehouse_product_id):
        user = request.user
        
        company = Company.objects.get(pk = int(company_id))
        
        if user.is_admin and (company.company_owner.id != user.id):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        elif user.is_employee and not (CompanyEmployee.objects.filter(companyid = int(company_id), employeeid = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        
        if not WarehouseProduct.objects.filter(pk = warehouse_product_id).exists():
            return Response({
                "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)
        
        warehouse_product = WarehouseProduct.objects.get(company=company_id, pk=warehouse_product_id)
        serializer = WarehouseProductSerializer(warehouse_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # Creating dict with errors, keys are field names, values are error messages
            errors = {}
            for field, error_detail in serializer.errors.items():
                errors[field] = error_detail[0]
                
            return Response({
                    "error": errors
                }, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, warehouse_product_id):
        user = request.user
        company = Company.objects.get(pk = int(company_id))
        
        if user.is_admin and (company.company_owner.id != user.id):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        elif user.is_employee and not (CompanyEmployee.objects.filter(companyid = int(company_id), employeeid = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
            
        if not WarehouseProduct.objects.filter(pk = warehouse_product_id).exists():
            return Response({
                "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)
        
        warehouse_product = WarehouseProduct.objects.get(company=company_id, pk=warehouse_product_id)
        warehouse_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WarehouseSummaryView(APIView):
    permission_classes = (EmployeeLevelPermission,)
    def get(self, request, company_id):
        user = request.user
        
        company = Company.objects.get(pk = company_id)
        
        if user.is_admin and (company.company_owner.id != user.id):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        elif user.is_employee and not (CompanyEmployee.objects.filter(companyid = int(company_id), employeeid = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)  
        
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