from itertools import product

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        result = Product.objects.filter(
            name__contains = "Smartphone"
        ).update(discount=10)
        print(result)
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
