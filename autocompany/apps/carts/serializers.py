from rest_framework import serializers

from autocompany.apps.carts.models import ShoppingCartItem


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        exclude = ('cart',)
