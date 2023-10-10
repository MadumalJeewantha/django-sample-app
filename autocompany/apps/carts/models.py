from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from autocompany.apps.products.models import Product
from autocompany.utils.time_stamp_mixin import TimeStampMixin


class ShoppingCart(TimeStampMixin):
    """
    Defines a single cart with its fields and properties.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return self.user


class ShoppingCartItem(models.Model):
    """
    Defines a single cart item with its fields and properties.
    """

    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    @property
    def total_price(self):
        return self.quantity * self.product_id.price

    def __str__(self):
        return self.cart
