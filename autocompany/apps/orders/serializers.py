from rest_framework import serializers

from autocompany.apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('user', 'order_date')
