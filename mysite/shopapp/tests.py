#from http.client import responses
#from itertools import product
from itertools import product

from django.test import TestCase
from django.urls import reverse
from string import ascii_letters
from random import choices

#from Forms.mysite.shopapp.views import products_list
from .models import Product, Order
from django.contrib.auth.models import User, Permission
from django.conf import settings
from .utils import add_num
from datetime import datetime


class AddNumTestCase(TestCase):
    def test_add_num(self):
        result = add_num(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="test_admin", password="qwerty")
        permission = Permission.objects.get(codename="add_product")
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)

    def test_create_product(self):
        self.product_name = "".join(choices(ascii_letters, k=10))
        #Product.objects.filter(name=self.product_name).delete()
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "1234",
                "discount": "10",
                "description": "A new table",
                "created_at": datetime.now(),
                "archived": 0,
                "created_by_id": self.user
            },
            HTTP_USER_AGENT="Mozilla/5.0"
        )
        self.assertTrue(Product.objects.filter(name=self.product_name).exists)
        self.assertRedirects(response, reverse("shopapp:products_list"))
        #self.product.delete()


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="test_admin", password="qwerty")
        permission = Permission.objects.get(codename="view_product")
        cls.user.user_permissions.add(permission)
        cls.product = Product.objects.create(name="Best product", created_by_id=cls.user.pk)

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()
        super().tearDownClass()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk}),
            HTTP_USER_AGENT="Mozilla/5.0"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_contant(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk}),
            HTTP_USER_AGENT="Mozilla/5.0"
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
        #'shopapp-fixture.json'
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'), HTTP_USER_AGENT="Mozilla/5.0")
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="test_admin", password="qwerty")
        permission = Permission.objects.get(codename="add_order")
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT="Mozilla/5.0")
        self.assertContains(response, "Orders")

    def test_orders_view_not_auth(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT="Mozilla/5.0")
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)
        self.assertRedirects(response, str(settings.LOGIN_URL)+"?next=/shop/orders/")


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:products_export'), HTTP_USER_AGENT="Mozilla/5.0")
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
            "pk": product.pk,
            "name": product.name,
            "price": str(product.price),
            "archived": product.archived,
#            "created_by": str(product.created_by)
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(products_data["products"], expected_data)


class OrderDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="test_admin", password="qwerty")
        permission = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)
        self.product = Product.objects.create(name="Best product", created_by_id=self.user.pk)
        self.order = Order.objects.create(
            user_id=self.user.pk,
            delivery_address="ул. Правды, д.10",
            promocode="321",
            #cls.order_product = .create(order_id=cls.order.pk, product_id=cls.product.pk)
        )
    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_get_order_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk}),
            HTTP_USER_AGENT="Mozilla/5.0"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertContains(response, self.user.pk)


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        "users-fixture.json",
        "products-fixture.json",
        "orders-fixture.json",
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:orders_export'), HTTP_USER_AGENT="Mozilla/5.0")
        self.assertEqual(response.status_code, 200)
        #products = Product.objects.order_by("pk").all()
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                #"created_at": order.created_at,
                "user_id": order.user_id,
                "products_id": [
                    {
                        "pk": product.pk,
                        "name": product.name,
                        "price": str(product.price),
                        "archived": product.archived,
                        #            "created_by": str(product.created_by)
                        }
                    for product in order.products.all()
                ]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data["orders"], expected_data)
