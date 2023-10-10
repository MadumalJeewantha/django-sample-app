from django.core.management.base import BaseCommand

from autocompany.apps.products.models import Product


class Command(BaseCommand):
    help = 'Seed the database with product data'

    def handle(self, *args, **kwargs):
        product_data = [
            {
                'product_code': 'VP-0001',
                'name': 'Engine Piston',
                'description': 'High-performance engine piston for all types of vehicles',
                'price': '89.99',
                'sku': 'ep-001',
                'quantity': 100,
            },
            {
                'product_code': 'VP-0002',
                'name': 'Brake Pads',
                'description': 'Quality brake pads for smooth and safe braking',
                'price': '24.99',
                'sku': 'bp-001',
                'quantity': 150,
            },
            {
                'product_code': 'VP-0003',
                'name': 'Transmission Fluid',
                'description': 'Premium transmission fluid for optimal gear shifting',
                'price': '19.95',
                'sku': 'tf-001',
                'quantity': 200,
            },
            {
                'product_code': 'VP-0004',
                'name': 'Spark Plugs',
                'description': 'High-quality spark plugs for efficient combustion',
                'price': '9.99',
                'sku': 'sp-001',
                'quantity': 300,
            },
            {
                'product_code': 'VP-0005',
                'name': 'Fuel Filter',
                'description': 'Fuel filter for clean and reliable fuel supply',
                'price': '14.50',
                'sku': 'ff-001',
                'quantity': 250,
            },
            {
                'product_code': 'VP-0006',
                'name': 'Air Filter',
                'description': 'High-performance air filter for improved engine efficiency',
                'price': '19.99',
                'sku': 'af-001',
                'quantity': 200,
            },
            {
                'product_code': 'VP-0007',
                'name': 'Tire Pressure Gauge',
                'description': 'Accurate tire pressure gauge for safe driving',
                'price': '8.95',
                'sku': 'tpg-001',
                'quantity': 300,
            },
            {
                'product_code': 'VP-0008',
                'name': 'Radiator Hose',
                'description': 'Durable radiator hose for efficient cooling',
                'price': '12.99',
                'sku': 'rh-001',
                'quantity': 150,
            },
            {
                'product_code': 'VP-0009',
                'name': 'Exhaust Muffler',
                'description': 'Quality exhaust muffler for reduced noise and emissions',
                'price': '34.99',
                'sku': 'em-001',
                'quantity': 100,
            },
            {
                'product_code': 'VP-0010',
                'name': 'Oxygen Sensor',
                'description': 'Precision oxygen sensor for efficient fuel management',
                'price': '29.99',
                'sku': 'os-001',
                'quantity': 120,
            },
        ]

        # Loop through the data and create Product objects
        for data in product_data:
            Product.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Product data seeded successfully!'))
