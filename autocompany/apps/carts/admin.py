from django.contrib import admin

from autocompany.apps.carts.models import ShoppingCart, ShoppingCartItem

admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
