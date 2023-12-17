from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company, Catalog, Product
from .serializers import CompanySerializer, CatalogSerializer, ProductSerializer


class CompanyListCreateView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyRetrieveUpdateDeleteView(APIView):
    def get(self, request, id):
        company = Company.objects.get(pk=id)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def patch(self, request, id):
        company = Company.objects.get(pk=id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        company = Company.objects.get(pk=id)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateView(APIView):
    def get(self, request, company_id):
        products = Product.objects.filter(company=company_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, company_id):
        request.data['company'] = company_id
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDeleteView(APIView):
    def get(self, request, company_id, product_id):
        try:
            product = Product.objects.get(company=company_id, pk=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, company_id, product_id):
        product = Product.objects.get(company=company_id, pk=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, product_id):
        product = Product.objects.get(company=company_id, pk=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CatalogListCreateView(APIView):
    def get(self, request, company_id):
        catalogs = Catalog.objects.filter(company=company_id)
        serializer = CatalogSerializer(catalogs, many=True)
        return Response(serializer.data)

    def post(self, request, company_id):
        request.data['company'] = company_id
        serializer = CatalogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CatalogRetrieveUpdateDeleteView(APIView):
    def get(self, request, company_id, catalog_id):
        try:
            catalog = Catalog.objects.get(company=company_id, pk=catalog_id)
            serializer = CatalogSerializer(catalog)
            return Response(serializer.data)
        except:
            return Response({"error": "Catalog not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, company_id, catalog_id):
        catalog = Catalog.objects.get(company=company_id, pk=catalog_id)
        serializer = CatalogSerializer(catalog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, catalog_id):
        catalog = Catalog.objects.get(company=company_id, pk=catalog_id)
        catalog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





