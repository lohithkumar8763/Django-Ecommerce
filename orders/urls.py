from django.urls import path

from . import views


urlpatterns = [

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "success/<int:order_id>/",
        views.order_success,
        name="order_success"
    ),

    path(
        "",
        views.my_orders,
        name="orders"
    ),

    path(
        "<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),
]