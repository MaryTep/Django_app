from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order


class Command(BaseCommand):
    """
    Creates orders
    """
    def handle(self, *args, **options):
        self.stdout.write("Create orders")
        user = User.objects.get(username='admin')
        orders = [
            {
                'delivery_address': 'ул. Правды, д.1',
                'promocode': 'SALE123',
                'user': user
            },
            {
                'delivery_address': 'ул. Правды, д.1',
                'promocode': '',
                'user': user
            }

        ]
        for order in orders:
            order, created = Order.objects.get_or_create(
                delivery_address=order['delivery_address'],
                promocode=order['promocode'],
                user=order['user']
            )
            self.stdout.write(f'Created order {order}')

        self.stdout.write(self.style.SUCCESS("Orders created"))
