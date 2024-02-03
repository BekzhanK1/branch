from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Avg
from .models import Company, Catalog, Product, Order
from customer.models import Attendance, Customer
from account.models import EmployeeUser
from account.serializers import EmployeeUserSerializer
from .serializers import CompanySerializer, CatalogSerializer, ProductSerializer, OrderSerializer
from permissions import permission


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_owner:
            return Company.objects.filter(company_owner=user)
        elif user.is_employee == user.company:
            return Company.objects.filter(pk=user.company)
        else:
            PermissionDenied("You don't have permission for this company")

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
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

    def retrieve(self, request, pk=None):
        company = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(company)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        if not request.user.is_owner:
            PermissionDenied("You don't have permission")

        company = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if not request.user.is_owner:
            PermissionDenied("You don't have permission")

        company = get_object_or_404(self.get_queryset(), pk=pk)
        self.perform_destroy(company)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        company_id = self.kwargs.get('company_id')

        if user.is_owner:
            company = get_object_or_404(
                Company, pk=company_id, company_owner=user)
            return Product.objects.filter(company=company)
        elif user.is_employee and company_id == user.company:
            return Product.objects.filter(company=user.company)
        else:
            PermissionDenied("You have no permission to access this company")

    def list(self, request, company_id=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, company_id=None):
        user = request.user
        if user.is_owner:
            company = get_object_or_404(
                Company, company_owner=user, pk=company_id)
        if user.is_employee:
            company = user.company
        data = request.data
        data['company'] = company.pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, company_id=None):
        queryset = self.get_queryset()
        product = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data)

    def partial_update(self, request, pk=None, company_id=None):
        queryset = self.get_queryset()
        product = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(
            product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None, company_id=None):
        queryset = self.get_queryset()
        product = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CatalogViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    serializer_class = CatalogSerializer

    def get_queryset(self):
        user = self.request.user
        company_id = self.kwargs.get('company_id')

        if user.is_owner:
            company = get_object_or_404(
                Company, pk=company_id, company_owner=user)
            return Catalog.objects.filter(company=company)
        elif user.is_employee and company_id == user.company:
            return Catalog.objects.filter(company=user.company)
        else:
            PermissionDenied("You have no permission to access this company")

    def list(self, request, company_id=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, company_id=None):
        user = request.user
        if user.is_owner:
            company = get_object_or_404(
                Company, company_owner=user, pk=company_id)
        if user.is_employee:
            company = user.company
        data = request.data
        data['company'] = company.pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, company_id=None):
        queryset = self.get_queryset()
        catalog = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(catalog)
        return Response(serializer.data)

    def partial_update(self, request, pk=None, company_id=None):
        queryset = self.get_queryset()
        catalog = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(
            catalog, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None, company_id=None):
        queryset = self.get_queryset()
        catalog = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(catalog)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        company_id = self.kwargs.get('company_id')

        if user.is_owner:
            company = get_object_or_404(
                Company, pk=company_id, company_owner=user)
            return Order.objects.filter(company=company)
        elif user.is_employee and company_id == user.company:
            return Order.objects.filter(company=user.company)
        else:
            PermissionDenied("You have no permission to access this company")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        # Perform any additional logic before creating the order
        serializer.save()

        customer = serializer.validated_data['customer']
        company = serializer.validated_data['company']
        order_time = serializer.validated_data['order_time']
        
        attendance = Attendance.objects.create(
            customer = customer,
            company = company,
            check_in_time = order_time
        )
        
        self.check_for_activity(customer)
        
    def check_for_activity(customer):
        number_of_visits = Attendance.objects.filter(customer = customer).count()
        if number_of_visits > settings.ACTIVE_CLIENT_VISITS:
            customer.status = Customer.CustomerStatus.ACTIVE_CLIENT
            customer.save()
            
            
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.AdminLevelPermission, )
    serializer_class = EmployeeUserSerializer
    
    def get_queryset(self):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        if user.is_owner:
            company = get_object_or_404(
                Company, pk=company_id, company_owner=user)
            return EmployeeUser.objects.filter(company = company)
        else:
            PermissionDenied("You have no permission to access this company")
    
    def list(self, request, company_id = None):
        serializer = self.serializer_class(self.get_queryset(), many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk = None, company_id = None):
        employee = get_object_or_404(self.get_queryset(), pk = pk)
        serializer = self.serializer_class(employee)
        return Response(serializer.data)
    
    def partial_update(self, request, pk = None, company_id = None):
        employee = get_object_or_404(self.get_queryset(), pk = pk)
        serializer = self.serializer_class(employee, data = request.data, partial = True)
        
        allowed_fields = ['position', 'salary']
        for field in request.data.keys():
            if field not in allowed_fields:
                serializer.validated_data.pop(field, None)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk = None, company_id = None):
        employee = get_object_or_404(self.get_queryset(), pk = pk)
        self.perform_destroy(employee)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail = False, methods=['get'])
    def analysis(self, request, company_id = None):
        
        employees = self.get_queryset()
        
        analysis_data = employees.aggregate(
                number_of_employees=Count('id'),
                total_salary=Sum('salary'),
                average_salary=Avg('salary')
        )

        return Response(analysis_data)
        
        

        
    