from django.contrib.auth.models import User
from django.db import models

from autocompany.apps.products.models import Product
from autocompany.utils.time_stamp_mixin import TimeStampMixin


class Order(TimeStampMixin):
    """
    Defines a single order with its fields and properties.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.user


class OrderItem(models.Model):
    """
    Defines a single order item with its fields and properties.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'

    def __str__(self):
        return self.order
