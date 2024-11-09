"""
В этом модуле лежат раличные наборы представлений.

Разные view интернет-магазина по товарам, заказам и т.д.
"""

import logging
from dataclasses import field
from itertools import product
from pickle import FALSE
# from itertools import product
from timeit import default_timer
from csv import DictWriter
from django.http import (HttpRequest, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.views import View
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.utils.translation import gettext as _
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .common import save_csv_products
from .models import Product, Order, ProductImage, User
from .forms import ProductForm, OrderForm, GroupForm
from .serializer import ProductSerializer, OrderSerializer

log = logging.getLogger(__name__)

@extend_schema(description="Product views CRUD")
class ProductViewSet (ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived"
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]
    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, return 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, reques: Request):
        response = HttpResponse(content_type="txt/csv")
        filename = "product-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
            "created_by_id"
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response,fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(methods=["post"], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        # print("hello products list")
        return super().list(*args, **kwargs)


class OrderViewSet (ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = ["delivery_address", "promocode", "user__username"]
    filterset_fields = [
        "delivery_address",
        "promocode",
        "user"
    ]
    ordering_fields = [
        "delivery_address",
        "promocode",
        "user"
    ]


class ShopIndexView(View):
    # @method_decorator(cache_page(60 * 3))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('laptop', 1999),
            ('desktop', 2999),
            ('smartphone', 999)
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
            'items': 5,
        }
        log.debug("Products for shop index: %s", product)
        log.info("Rendering shop index")
        print("shop index context", context)
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm,
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

# class ProductsListView(TemplateView):
#     template_name = 'shopapp/products-list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         return context
#
# def products_list(request: HttpRequest):
#     context = {
#         'products': Product.objects.all(),
#     }
#     return render(request, 'shopapp/products-list.html', context=context)


# def orders_list(request: HttpRequest):
#     context = {
#         'orders': Order.objects.select_related('user').prefetch_related('products').all(),
#     }
#     return render(request, 'shopapp/order_list.html', context=context)


class ProductDetailsView(DetailView):

    template_name = "shopapp/product-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductCreateView(UserPassesTestMixin, CreateView):

    def test_func(self):
        return self.request.user.has_perm('shopapp.add_product')
        #return self.request.user.user_permissions.filter(name="add_product").exists()

    # class ProductCreateView(UserPassesTestMixin, CreateView):
    #
    #     def test_func(self):
    #         return self.request.user.groups.filter(name="Add_product").exists()

    model = Product
    # fields = "name", "price", "discount", "description", "preview"
    form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        product = self.get_object()
        response = (self.request.user.is_superuser or
                    (self.request.user.has_perm('shopapp.change_product') and
                     product.created_by == self.request.user))
        return response

    model = Product
    # fields = "name", "price", "discount", "description", "preview"
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class LatestProductsFeed(Feed):
    title = "Blog products (latest)"
    description = "Updates on change and addition"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
            Product.objects
            .filter(archived=False)
            .order_by("-created_at")[:5]
        )

    def item_name(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#         else:
#             form = ProductForm()
#
#     context = {
#         "forms": form,
#     }
#     return render(request, 'shopapp/create-product.html', context=context)
#
#

class OrdersListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.select_related('user').prefetch_related('products')


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order",
    template_name = "shopapp/order-details.html"
    queryset = Order.objects.select_related('user').prefetch_related('products')
    context_object_name = "order"

# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return redirect(url)
#         else:
#             form = OrderForm()
#
#     context = {
#         "forms": form,
#     }
#     return render(request, 'shopapp/create-order.html', context=context)


class OrderCreateView(CreateView):
    model = Order
    #queryset = Order.objects.select_related('user').prefetch_related('products')
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data  is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
    #                "created_by": product.created_by
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        return JsonResponse({"products": products_data})


class OrdersDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                # "created_at": order.created_at,
                "user_id": order.user_id,
                "products_id": [
                    {
                        "pk": product.pk,
                        "name": product.name,
                        "price": product.price,
                        "archived": product.archived,
                        #            "created_by": str(product.created_by)
                    }
                    for product in order.products.all()
                ]
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


class UserOrdersListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')
    def get(self, request: HttpRequest, user_id) -> JsonResponse:
        # Получаем пользователя
        cache_key = "user_orders_list_view"
        orders_data = cache.get(cache_key)
        if orders_data is not None and orders_data["user"]["id"] == user_id:
            return JsonResponse({"orders": orders_data})
        owner = get_object_or_404(User, pk=user_id)
        # print("!!!!", "Новый кэш")
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                # "user_id": order.user_id,
                # "user_name":order.user.username,
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                # "created_at": order.created_at,
                "products_id": [
                    {
                        "pk": product.pk,
                        "name": product.name,
                        "price": product.price,
                        "archived": product.archived,
                        #            "created_by": str(product.created_by)
                    }
                    for product in order.products.all()
                ]
            }
            for order in orders if order.user_id == user_id
        ]
        orders_data = {
            "user": {
                "id": owner.id,
                "username": owner.username,
                "email": owner.email,

            },
            "orders": orders_data
        }
        cache.set(cache_key, orders_data, 300)
        return JsonResponse({"orders": orders_data})
