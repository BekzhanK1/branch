from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from permissions import permission
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Customer, Attendance
from company.models import Company
from .serializers import CustomerSerializer, AttendanceSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        
        if not user.is_owner and not user.is_employee:
            raise PermissionDenied("You don't have permission to this company")
        
        company_id = self.kwargs.get('company_id')
        
        if user.is_owner:
            company = get_object_or_404(Company, pk = company_id, company_owner = user)
        
        elif user.is_employee and user.company == company_id:
            company =  get_object_or_404(Company, pk = user.company)
            
        customers = Customer.objects.filter(attendance__company = company).select_related('user').distinct()
        return customers

    def list(self, request, company_id = None):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def create(self, request):
    #     data = request.data
    #     serializer = self.serializer_class(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, company_id = None):
        customer = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(customer)
        return Response(serializer.data)
    

    # def partial_update(self, request, pk=None):
    #     customer = get_object_or_404(self.get_queryset(), pk=pk)
    #     serializer = self.serializer_class(customer, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # def destroy(self, request, id=None):
    #     customer = get_object_or_404(self.queryset, pk=id)
    #     self.perform_destroy(customer)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = (permission.EmployeeLevelPermission, )
    
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        
        if not user.is_owner and not user.is_employee:
            raise PermissionDenied("You don't have permission to this company")
        
        company_id = self.kwargs.get('company_id')
        
        if user.is_owner:
            company = get_object_or_404(Company, pk = company_id, company_owner = user)
        
        elif user.is_employee and user.company == company_id:
            company =  get_object_or_404(Company, pk = user.company)
            
        return Attendance.objects.filter(company = company)
          
    
      
    def list(self, request, company_id = None):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def partial_update(self, request, pk=None):
    #     attendance = get_object_or_404(self.queryset, pk=pk)
    #     serializer = self.serializer_class(attendance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    def retrieve(self, request, pk = None, company_id = None):
        attendance = get_object_or_404(self.get_queryset(), pk = pk)
        serializer = self.serializer_class(attendance)
        return Response(serializer.data)
    
