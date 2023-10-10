from django.db import models

from autocompany.utils.time_stamp_mixin import TimeStampMixin


class Product(TimeStampMixin):
    """
    Defines a single product with its fields and properties.
    """

    product_code = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sku = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True)
    # Introduce product category as an improvement

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
