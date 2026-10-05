from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product


def _get_cart(request):

    return request.session.get(
        "cart",
        {}
    )


def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart = _get_cart(request)

    product_id = str(product_id)


    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1


    if cart[product_id] > product.stock:

        cart[product_id] = product.stock

        messages.warning(
            request,
            "You cannot add more than the available stock."
        )


    request.session["cart"] = cart

    request.session.modified = True

    return redirect("cart")


def decrease_quantity(request, product_id):

    cart = _get_cart(request)

    product_id = str(product_id)


    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:

            del cart[product_id]


    request.session["cart"] = cart

    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):

    cart = _get_cart(request)

    product_id = str(product_id)


    if product_id in cart:

        del cart[product_id]


    request.session["cart"] = cart

    request.session.modified = True

    return redirect("cart")


def cart_view(request):

    cart = _get_cart(request)

    items = []

    total = 0


    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal


        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )


    return render(
        request,
        "cart/cart.html",
        {
            "items": items,
            "total": total,
        }
    )


def clear_cart(request):

    request.session["cart"] = {}

    request.session.modified = True

    return redirect("cart")