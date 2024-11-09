from itertools import product

from django.core.management import BaseCommand
from django.db.models import Avg, Min, Max, Count, Sum

from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo aggregate actions")

        orders = Order.objects.annotate(
            total = Sum("products__price", default=0),
            products_count = Count("products"),
        )
        for order in orders:
            print(
                f'Order #{order.id}'
                f' with {order.products_count}'
                f' products worth {order.total}'
            )
        # result = Product.objects.filter(
        #     name__contains = "Smartphone"
        # ).aggregate(
        #     Avg("price"),
        #     Min("price"),
        #     max_price=Max("price"),
        #     count=Count("id")
        # )
        # print(result)
        # user = User.objects.get(username="Ry-ry")
        # info = [
        #     ("Smartphone 1", 199, user),
        #     ("Smartphone 2", 299, user),
        #     ("Smartphone 3", 399, user),
        # ]
        # products = [
        #     Product(name=name, price=price, created_by=created_by)
        #     for name, price, created_by in info
        # ]
        #
        # result = Product.objects.bulk_create(products)
        # for obj in result:
        #     print(obj)
        #
        self.stdout.write("Done")
