from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from company.permissions import *
from company.models import Company, CompanyEmployee

class MenuItemListCreateView(APIView): 
    permission_classes = (EmployeeLevelPermission, )
    def get(self, request, company_id):
        user = request.user

        company = Company.objects.get(pk = int(company_id))
        if user.is_admin and (company.company_owner.id != user.id): 
            return Response({
                "error": "you don't have permission for this company"
            }, status = status.HTTP_403_FORBIDDEN)
        elif user.is_employee and not (CompanyEmployee.objects.filter(companyid = int(company_id), employeeid = int(user.id)).exists()):
            return Response({
                "error": "You don't have permission for this company"
            }, status=status.HTTP_403_FORBIDDEN)
        menu_item = MenuItem.objects.filter(company = company)
        serializer = MenuItemSerializer(menu_item, many = True)
        return Response(serializer.data)

    def post(self, request, company_id): 
        user = request.user

        company = Company.objects.get(pk = int(company_id))

        if user.is_admin and (company.company_owner.id != user.id): 
            return Response({
                "Error": "You don't have permission for this company"
            }, status=status.HTTP_403_FORBIDDEN)
        elif user.is_employee and not(CompanyEmployee.objects.filter(companyid = int(company_id), employeeid = int(user.id)).exists()):
            return Response({
                "Error": "You don't have permission for this company"
            }, status=status.HTTP_403_FORBIDDEN)
        
        request.data['company'] = company_id
        serializer = MenuItemSerializer(data = request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class MenuItemRetrieveUpdateDeleteView(APIView):
    def get(self, request, company_id, menu_item_id):
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
        if not MenuItem.objects.filter(pk = menu_item_id).exists():
            return Response({
            "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)
            
        menu_item = MenuItem.objects.get(company=company_id, pk=menu_item_id)
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)

    def patch(self, request, company_id, menu_item_id):
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
        
        if not MenuItem.objects.filter(pk = menu_item_id).exists():
            return Response({
                "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)
        
        menu_item = MenuItem.objects.get(company=company_id, pk=menu_item_id)
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
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

    def delete(self, request, company_id, menu_item_id):
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
            
        if not MenuItem.objects.filter(pk = menu_item_id).exists():
            return Response({
                "error": "Such product does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)
        
        menu_item = MenuItem.objects.get(company=company_id, pk=menu_item_id)
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoryListCreateView(APIView):
    
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

        category = Category.objects.filter(company=company)
        serializer = CategorySerializer(category, many=True)
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
        serializer = CategorySerializer(data=request.data)
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


class CategorygRetrieveUpdateDeleteView(APIView):
    def get(self, request, company_id, category_id):
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
            
        if not Category.objects.filter(pk = category_id, company__id = company_id).exists():
            return Response({
                "error": "Such category does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)
            
        category = Category.objects.get(company=company, pk=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
        

    def patch(self, request, company_id, category_id):
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
            
        if not Category.objects.filter(pk = category_id, company__id = company_id).exists():
            return Response({
                "error": "Such category does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)

        category = Category.objects.get(company=company, pk=category_id)
        serializer = CategorySerializer(category, data=request.data, partial=True)
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
        

    def delete(self, request, company_id, category_id):
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
            
        if not Category.objects.filter(pk = category_id, company__id = company_id).exists():
            return Response({
                "error": "Such category does not exist"
            }, status = status.HTTP_400_BAD_REQUEST)

        category = Category.objects.get(company=company, pk=category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
