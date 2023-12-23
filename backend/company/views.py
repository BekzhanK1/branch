from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company, Catalog, Product, CompanyEmployee
from .serializers import CompanySerializer, CatalogSerializer, ProductSerializer


class CompanyListCreateView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        if not user.is_admin or user.is_employee:
            return Response({'error': "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data['company_owner'] = user.pk
        serializer = CompanySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyRetrieveUpdateDeleteView(APIView):
    def get(self, request):
        user = request.user

        if user.is_superadmin or user.is_admin:
            company = Company.objects.get(company_owner=user)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        else:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )

    def patch(self, request):
        user = request.user

        if user.is_superadmin or user.is_admin:
            company = Company.objects.get(company_owner=user)
            serializer = CompanySerializer(
                company, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )

    def delete(self, request):
        user = request.user

        if user.is_superadmin:
            company = Company.objects.get(pk=id)
            company.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'error': "You don't have a permission"},
                status=status.HTTP_403_FORBIDDEN
            )


class ProductListCreateView(APIView):

    def get(self, request):
        user = request.user

        if user is not None:
            if user.is_employee:
                employee = CompanyEmployee.objects.get(employee=user)
                company = employee.company
            elif user.is_admin:
                company = Company.objects.get(company_owner=user)
            products = Product.objects.filter(company=company)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'error': "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def post(self, request):
        user = request.user

        if user is not None:

            if user.is_employee:
                employee = CompanyEmployee.objects.get(employee=user)
                company = employee.company
            elif user.is_admin:
                company = Company.objects.get(company_owner=user)

            request.data['company'] = company.id
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ProductRetrieveUpdateDeleteView(APIView):
    def get(self, request, product_id):
        user = request.user

        if user is not None:
            if user.is_employee:
                employee = CompanyEmployee.objects.get(employee=user)
                company = employee.company
            elif user.is_admin:
                company = Company.objects.get(company_owner=user)

            try:
                product = Product.objects.get(company=company, pk=product_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {'error': "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def patch(self, request, product_id):
        user = request.user

        if user is not None:
            if user.is_employee:
                employee = CompanyEmployee.objects.get(employee=user)
                company = employee.company
            elif user.is_admin:
                company = Company.objects.get(company_owner=user)

            try:
                product = Product.objects.get(company=company, pk=product_id)
                serializer = ProductSerializer(
                    product, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            except:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def delete(self, request, product_id):
        user = request.user

        if user is not None:
            if user.is_employee:
                employee = CompanyEmployee.objects.get(employee=user)
                company = employee.company
            elif user.is_admin:
                company = Company.objects.get(company_owner=user)

            try:
                product = Product.objects.get(company=company, pk=product_id)
                product.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {'error': "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class CatalogListCreateView(APIView):
    def get(self, request):
        user = request.user

        if user.is_employee:
            employee = CompanyEmployee.objects.get(employee=user)
            company = employee.company
        elif user.is_admin:
            company = Company.objects.get(company_owner=user)

        catalogs = Catalog.objects.filter(company=company)
        serializer = CatalogSerializer(catalogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        if user.is_employee:
            employee = CompanyEmployee.objects.get(employee=user)
            company = employee.company
        elif user.is_admin:
            company = Company.objects.get(company_owner=user)


        request.data['company'] = company.id
        serializer = CatalogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CatalogRetrieveUpdateDeleteView(APIView):
    def get(self, request, catalog_id):
        user = request.user

        if user is not None:
            if user.is_employee:
                employee = CompanyEmployee.objects.get(employee=user)
                company = employee.company
            elif user.is_admin:
                company = Company.objects.get(company_owner=user)
            try:
                catalog = Catalog.objects.get(company=company, pk=catalog_id)
                serializer = CatalogSerializer(catalog)
                return Response(serializer.data)
            except:
                return Response({"error": "Catalog not found"}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            return Response(
                {'error': "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )


    def patch(self, request, catalog_id):
        user = request.user

        if user is not None:
            if user.is_employee:
                employee = CompanyEmployee.objects.get(employee=user)
                company = employee.company
            elif user.is_admin:
                company = Company.objects.get(company_owner=user)

            catalog = Catalog.objects.get(company=company, pk=catalog_id)
            serializer = CatalogSerializer(
                catalog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(
                {'error': "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def delete(self, request, catalog_id):
        user = request.user

        if user is not None:

            if user.is_employee:
                employee = CompanyEmployee.objects.get(employee=user)
                company = employee.company
            elif user.is_admin:
                company = Company.objects.get(company_owner=user)

            catalog = Catalog.objects.get(company=company, pk=catalog_id)
            catalog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        else:
            return Response(
                {'error': "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
