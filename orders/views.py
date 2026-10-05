from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.views import _get_cart
from store.models import Product

from .models import Order, OrderItem


@login_required
def checkout(request):

    cart = _get_cart(request)

    if not cart:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("cart")


    items = []

    total = Decimal("0.00")


    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id,
            available=True
        )


        quantity = min(
            quantity,
            product.stock
        )


        if quantity <= 0:
            continue


        subtotal = product.price * quantity

        total += subtotal


        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )


    if request.method == "POST":

        if not items:

            messages.error(
                request,
                "No valid products in cart."
            )

            return redirect("cart")


        with transaction.atomic():

            # Check stock again before creating order
            for item in items:

                product = Product.objects.select_for_update().get(
                    id=item["product"].id
                )

                if product.stock < item["quantity"]:

                    messages.error(
                        request,
                        f"Not enough stock for {product.name}."
                    )

                    return redirect("cart")


            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                status="pending"
            )


            for item in items:

                product = Product.objects.select_for_update().get(
                    id=item["product"].id
                )


                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    price=product.price
                )


                # Reduce stock
                product.stock -= item["quantity"]


                if product.stock == 0:

                    product.available = False


                product.save(
                    update_fields=[
                        "stock",
                        "available"
                    ]
                )


        # Clear cart
        request.session["cart"] = {}

        request.session.modified = True


        return redirect(
            "payment",
            order_id=order.id
        )


    return render(
        request,
        "orders/checkout.html",
        {
            "items": items,
            "total": total,
        }
    )


@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )


    return render(
        request,
        "orders/order_success.html",
        {
            "order": order
        }
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items__product"
    ).order_by(
        "-created_at"
    )


    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        id=order_id,
        user=request.user
    )


    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order
        }
    )