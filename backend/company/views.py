from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Company, Catalog, Product, CompanyEmployee
from .serializers import CompanySerializer, CatalogSerializer, ProductSerializer
from permissions import permission


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    serializer_class = CompanySerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_owner:
            return Company.objects.filter(company_owner = user)
        elif user.is_employee == user.company:
            return Company.objects.filter(company = user.company)
        else:
            PermissionDenied("You don't have permission for this company")
            
    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        if not request.user.is_owner:
            PermissionDenied("You don't have permission")
        
        data = request.data
        data['company_owner'] = request.user.pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk = None):
        company = get_object_or_404(self.get_queryset(), pk = pk)
        serializer = self.serializer_class(company)
        return Response(serializer.data)
    
    def partial_update(self, request, pk = None):
        if not request.user.is_owner:
            PermissionDenied("You don't have permission")
        
        company = get_object_or_404(self.get_queryset(), pk = pk)
        serializer = self.serializer_class(company, data = request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk = None):
        if not request.user.is_owner:
            PermissionDenied("You don't have permission")
        
        company = get_object_or_404(self.get_queryset(), pk = pk)
        self.perform_destroy(company)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateView(APIView):
    
    permission_classes = (permission.EmployeeLevelPermission, )

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

        products = Product.objects.filter(company=company)
        serializer = ProductSerializer(products, many=True)
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

        request.data['company'] = company.id
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       


class ProductRetrieveUpdateDeleteView(APIView):
    def get(self, request, company_id, product_id):
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

        if not Product.objects.filter(pk = product_id).exists():
            return Response({
                "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)

        
        product = Product.objects.get(company=company, pk=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
        
    def patch(self, request, company_id, product_id):
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
            
        if not Product.objects.filter(pk = product_id).exists():
            return Response({
                "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(company=company, pk=product_id)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
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

    def delete(self, request, company_id, product_id):
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
            
        if not Product.objects.filter(pk = product_id).exists():
            return Response({
                "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(company=company, pk=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CatalogListCreateView(APIView):
    
    permission_classes = (permission.EmployeeLevelPermission, )
    
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

        catalogs = Catalog.objects.filter(company=company)
        serializer = CatalogSerializer(catalogs, many=True)
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

        request.data['company'] = company.id
        serializer = CatalogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Creating dict with errors, keys are field names, values are error messages
            errors = {}
            for field, error_detail in serializer.errors.items():
                errors[field] = error_detail[0]
                
            return Response({
                    "error": errors
                }, status = status.HTTP_400_BAD_REQUEST)


class CatalogRetrieveUpdateDeleteView(APIView):
    def get(self, request, company_id, catalog_id):
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
            
        if not Catalog.objects.filter(pk = catalog_id, company__id = company_id).exists():
            return Response({
                "error": "Such catalog does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)
            
        catalog = Catalog.objects.get(company=company, pk=catalog_id)
        serializer = CatalogSerializer(catalog)
        return Response(serializer.data)
        

    def patch(self, request, company_id, catalog_id):
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
            
        if not Catalog.objects.filter(pk = catalog_id, company__id = company_id).exists():
            return Response({
                "error": "Such catalog does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)

        catalog = Catalog.objects.get(company=company, pk=catalog_id)
        serializer = CatalogSerializer(
            catalog, data=request.data, partial=True)
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
        

    def delete(self, request, company_id, catalog_id):
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
            
        if not Catalog.objects.filter(pk = catalog_id, company__id = company_id).exists():
            return Response({
                "error": "Such catalog does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)

        catalog = Catalog.objects.get(company=company, pk=catalog_id)
        catalog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
