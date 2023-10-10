from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Product

AUTH_ENDPOINT = '/api/auth/token/'


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {
            'id': 1,
            'product_code': 'P-1000',
            'name': 'Test Product',
            'description': 'Test Product description',
            'price': 100.50,
            'sku': 'items',
            'quantity': 100,
        }
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')

    def test_create_product_with_authentication(self):
        # Obtain a JWT token for the user
        response = self.client.post(AUTH_ENDPOINT, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract the access token from the response
        access_token = response.data['access']

        # Set the JWT token in the client's HTTP Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Make an authenticated POST request to create a product
        response = self.client.post('/api/v1/products/', self.product_data, format='json')

        # Assert that the response status code is HTTP 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_product_list(self):
        Product.objects.create(**self.product_data)
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        product = Product.objects.create(**self.product_data)
        response = self.client.get(f'/api/v1/products/{product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        product = Product.objects.create(**self.product_data)
        updated_data = {'name': 'Updated Product', 'description': 'Updated Description', 'price': 20.0}

        # Obtain a JWT token for the user
        response = self.client.post(AUTH_ENDPOINT, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract the access token from the response
        access_token = response.data['access']

        # Set the JWT token in the client's HTTP Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.patch(f'/api/v1/products/{product.pk}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(pk=product.pk).name, 'Updated Product')

    def test_delete_product(self):
        product = Product.objects.create(**self.product_data)

        # Obtain a JWT token for the user
        response = self.client.post(AUTH_ENDPOINT, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract the access token from the response
        access_token = response.data['access']

        # Set the JWT token in the client's HTTP Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.delete(f'/api/v1/products/{product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
