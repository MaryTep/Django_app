from django.urls import path, include
from django.views.decorators.cache import cache_page

from rest_framework.routers import DefaultRouter

from .views import (
                    ShopIndexView,
                    GroupsListView,
                    ProductDetailsView,
                    ProductsListView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    OrdersListView,
                    OrderDetailsView,
                    OrderCreateView,
                    OrderUpdateView,
                    OrderDeleteView,
                    ProductsDataExportView,
                    OrdersDataExportView,
                    ProductViewSet,
                    OrderViewSet,
                    LatestProductsFeed,
                    UserOrdersListView,

                    )

app_mame = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    # path('', cache_page(60 * 3)(ShopIndexView.as_view()), name='index'),
    path('', ShopIndexView.as_view(), name='index'),
    path('api/', include(routers.urls)),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/export/', ProductsDataExportView.as_view(), name='products_export'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/export/', OrdersDataExportView.as_view(), name='orders_export'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order_details'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/archive/', OrderDeleteView.as_view(), name='order_delete'),

    path("products/latest/feed/", LatestProductsFeed(), name="product-feed"),

    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='users_orders'),

]
