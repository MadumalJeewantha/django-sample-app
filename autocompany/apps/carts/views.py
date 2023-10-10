from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from autocompany.apps.carts.models import ShoppingCart, ShoppingCartItem
from autocompany.apps.carts.serializers import ShoppingCartItemSerializer
from autocompany.apps.products.models import Product


class ShoppingCartItemViewSet(ReadOnlyModelViewSet, CreateModelMixin, DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = ShoppingCartItem.objects.all()
    serializer_class = ShoppingCartItemSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # Default to 1 if quantity is not provided

        product = get_object_or_404(Product, pk=product_id)

        # Check if the user already has a cart, if not, create one
        cart, created = ShoppingCart.objects.get_or_create(user=user)

        # Check if the product is already in the cart, if so, update the quantity
        cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, product_id=product)
        cart_item.quantity += quantity

        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
