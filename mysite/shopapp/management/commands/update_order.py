from django.core.management import BaseCommand
from shopapp.models import Product, Order

class Command(BaseCommand):
    """
    Creates orders
    """
    def handle(self, *args, **options):
        self.stdout.write("Update orders")
        order = Order.objects.last()
        if not order:
            self.stdout.write("Заказов еще нет")
            return
        products = Product.objects.all()
        for product in products:
            order.products.add(product)

            order.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully added product {order.products.all()}"))
