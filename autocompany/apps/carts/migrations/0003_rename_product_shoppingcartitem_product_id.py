# Generated by Django 4.2.5 on 2023-10-03 13:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('carts', '0002_remove_shoppingcart_is_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcartitem',
            old_name='product',
            new_name='product_id',
        ),
    ]