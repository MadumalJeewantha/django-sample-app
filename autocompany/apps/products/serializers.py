from rest_framework import serializers

from autocompany.apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_code', 'name', 'description', 'price', 'sku', 'quantity']

    id = serializers.ReadOnlyField()
