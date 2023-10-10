from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from autocompany.apps.carts.models import ShoppingCart, ShoppingCartItem
from autocompany.apps.orders.models import Order, OrderItem
from autocompany.apps.orders.serializers import OrderSerializer


class SubmitOrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        delivery_date = self.request.data.get('delivery_date')

        try:
            ShoppingCart.objects.get(user=user)
        except ShoppingCart.DoesNotExist:
            raise NotFound('Shopping cart not found for the user.')

        # Create the order
        order = serializer.save(user=user, delivery_date=delivery_date)

        # Move products from the shopping cart to order items
        move_cart_items_to_order_items(order=order, user=user)


def move_cart_items_to_order_items(order, user):
    """
    move cart items to order items for the given user
    """

    try:
        cart = ShoppingCart.objects.get(user=user)
        cart_items = ShoppingCartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            product = cart_item.product_id
            quantity = cart_item.quantity

            # Create an OrderItem for each cart item
            order_item = OrderItem(
                order=order,
                product=product,
                quantity=quantity,
            )
            order_item.save()

            # Deduct the quantity from the product
            product.quantity -= quantity
            product.save()

        # Clear the shopping cart after moving items to orders
        cart.delete()

    except ShoppingCart.DoesNotExist:
        return 'Shopping cart not found for the user.'
    except Order.DoesNotExist:
        return 'Order not found.'
