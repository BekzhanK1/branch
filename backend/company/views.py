from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company, Catalog, Product, CompanyEmployee
from .serializers import CompanySerializer, CatalogSerializer, ProductSerializer
from .permissions import *

class CompanyListCreateView(APIView):
    
    permission_classes = (AdminLevelPermission, )
    
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        data = request.data
        data['company_owner'] = user.pk
        serializer = CompanySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyRetrieveUpdateDeleteView(APIView):
    
    permission_classes = (AdminLevelPermission, )
    
    def get(self, request, company_id):
        user = request.user

        company = Company.objects.get(pk = int(company_id))
        
        if company.company_owner.id != user.id:
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
            
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    
    def patch(self, request, company_id):
        user = request.user

        company = Company.objects.get(pk = int(company_id))
        
        if company.company_owner.id != user.id:
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        
        serializer = CompanySerializer(
            company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id):
        user = request.user

        company = Company.objects.get(pk=id)
        
        if company.company_owner.id != user.id:
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        
        company.delete()
        return Response(status=status.HTTP_200_OK)


class ProductListCreateView(APIView):
    
    permission_classes = (EmployeeLevelPermission, )

    def get(self, request, company_id):
        user = request.user
        
        company = Company.objects.get(pk = int(company_id))
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)

        products = Product.objects.filter(company=company)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    def post(self, request, company_id):
        user = request.user
        
        company = Company.objects.get(pk = int(company_id))
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
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
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
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
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
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
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
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
    
    permission_classes = (EmployeeLevelPermission, )
    
    def get(self, request, company_id):
        user = request.user

        company = Company.objects.get(pk = int(company_id))
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)

        catalogs = Catalog.objects.filter(company=company)
        serializer = CatalogSerializer(catalogs, many=True)
        return Response(serializer.data)

    def post(self, request, company_id):
        user = request.user

        company = Company.objects.get(pk = int(company_id))
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
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
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
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
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
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
        
        if not (company.company_owner.id != user.id) or not (CompanyEmployee.objects.filter(company__id = int(company_id), employee__id = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
            
        if not Catalog.objects.filter(pk = catalog_id, company__id = company_id).exists():
            return Response({
                "error": "Such catalog does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)

        catalog = Catalog.objects.get(company=company, pk=catalog_id)
        catalog.delete()
        
