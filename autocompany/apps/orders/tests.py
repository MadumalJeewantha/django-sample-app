from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from autocompany.apps.carts.models import ShoppingCart, ShoppingCartItem
from autocompany.apps.orders.models import Order, OrderItem
from autocompany.apps.products.models import Product


class SubmitOrderViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.product_1 = {
            'id': 1,
            'product_code': 'P-1000',
            'name': 'Test Product 1',
            'description': 'Test Product description',
            'price': 10,
            'sku': 'items',
            'quantity': 20,
        }

        self.product_2 = {
            'id': 2,
            'product_code': 'P-2000',
            'name': 'Test Product 2',
            'description': 'Test Product description',
            'price': 15,
            'sku': 'items',
            'quantity': 30,
        }

    def test_submit_order(self):
        # Create a shopping cart for the user
        cart = ShoppingCart.objects.create(user=self.user)

        # Add items to the shopping cart
        product1 = Product.objects.create(**self.product_1)
        ShoppingCartItem.objects.create(cart=cart, product_id=product1, quantity=3)

        product2 = Product.objects.create(**self.product_2)
        ShoppingCartItem.objects.create(cart=cart, product_id=product2, quantity=2)

        # Define the payload for submitting an order
        payload = {
            'user': self.user.id,
            'delivery_date': '2023-10-15T12:00:00Z',
        }

        # Submit the order
        response = self.client.post(reverse('submit-order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the order has been created
        order = Order.objects.get(user=self.user)
        self.assertIsNotNone(order)

        # Check if order items have been created
        order_items = OrderItem.objects.filter(order=order)
        self.assertEqual(len(order_items), 2)

        # Check if product quantities have been updated
        product1.refresh_from_db()
        product2.refresh_from_db()
        self.assertEqual(product1.quantity, 17)  # Initial quantity - 3
        self.assertEqual(product2.quantity, 28)  # Initial quantity - 2

        # Check if the shopping cart is empty
        cart_items = ShoppingCartItem.objects.filter(cart=cart)
        self.assertEqual(len(cart_items), 0)

    def test_submit_order_no_cart(self):
        # Define the payload for submitting an order
        payload = {
            'user': self.user.id,
            'delivery_date': '2023-10-15T12:00:00Z',
        }

        # Submit the order when the user has no shopping cart
        response = self.client.post(reverse('submit-order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
