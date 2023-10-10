from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from autocompany.apps.products.models import Product
from autocompany.apps.products.serializers import ProductSerializer


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a superadmin
        return request.user.is_superuser


class ProductListView(ListCreateAPIView):
    """
    Retrieve all Products, or create a new product.
    """

    serializer_class = ProductSerializer

    def get_permissions(self):
        # Restrict product create for unauthenticated requests.
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsSuperAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset.order_by('id')

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Product instance.
    """

    serializer_class = ProductSerializer

    def get_permissions(self):
        # Restrict product update and delete for unauthenticated requests.
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), IsSuperAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs.get('pk'))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductSerializer(instance)
        return Response(serializer.data)
