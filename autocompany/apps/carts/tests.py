from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from autocompany.apps.carts.models import ShoppingCart, ShoppingCartItem
from autocompany.apps.products.models import Product


class ShoppingCartItemViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        product_data = {
            'id': 1,
            'product_code': 'P-1000',
            'name': 'Test Product 1',
            'description': 'Test Product description',
            'price': 10,
            'sku': 'items',
            'quantity': 10,
        }
        self.product = Product.objects.create(**product_data)

    def test_create_shopping_cart_item(self):
        # Define the payload for creating a shopping cart item
        payload = {
            'product_id': self.product.id,
            'quantity': 3,
        }

        # Create a shopping cart item
        response = self.client.post(reverse('shoppingcartitem-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the shopping cart item has been created
        cart_item = ShoppingCartItem.objects.get(cart__user=self.user, product_id=self.product)
        self.assertEqual(cart_item.quantity, 3)

    def test_create_shopping_cart_item_existing_cart(self):
        # Create a shopping cart for the user
        cart = ShoppingCart.objects.create(user=self.user)

        # Define the payload for creating a shopping cart item
        payload = {
            'product_id': self.product.id,
            'quantity': 3,
        }

        # Create a shopping cart item with an existing cart
        response = self.client.post(reverse('shoppingcartitem-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the shopping cart item has been created in the existing cart
        cart_item = ShoppingCartItem.objects.get(cart=cart, product_id=self.product)
        self.assertEqual(cart_item.quantity, 3)

    def test_destroy_shopping_cart_item(self):
        # Create a shopping cart for the user
        cart = ShoppingCart.objects.create(user=self.user)

        # Create a shopping cart item
        cart_item = ShoppingCartItem.objects.create(cart=cart, product_id=self.product, quantity=2)

        # Delete the shopping cart item
        response = self.client.delete(reverse('shoppingcartitem-detail', args=[cart_item.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the shopping cart item has been deleted
        with self.assertRaises(ShoppingCartItem.DoesNotExist):
            ShoppingCartItem.objects.get(pk=cart_item.id)
