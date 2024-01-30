from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from permissions import permission
from django.shortcuts import get_object_or_404
from .models import Customer, Attendance
from .serializers import CustomerSerializer, AttendanceSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        customer = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(customer)
        return Response(serializer.data)
    

    def partial_update(self, request, pk=None):
        customer = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, id=None):
        customer = get_object_or_404(self.queryset, pk=id)
        self.perform_destroy(customer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        attendance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(attendance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
