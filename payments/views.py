from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from orders.models import Order

from .models import Payment


@login_required
def payment_page(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )


    if order.status == "paid":

        return redirect(
            "order_success",
            order_id=order.id
        )


    if request.method == "POST":

        method = request.POST.get(
            "method"
        )


        if method not in {
            "upi",
            "card",
            "cod"
        }:

            messages.error(
                request,
                "Please select a payment method."
            )

            return redirect(
                "payment",
                order_id=order.id
            )


        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "method": method,
                "amount": order.total_amount,
            }
        )


        payment.method = method

        payment.amount = order.total_amount

        payment.status = "paid"

        payment.paid_at = timezone.now()

        payment.save()


        order.status = "paid"

        order.save(
            update_fields=[
                "status"
            ]
        )


        messages.success(
            request,
            "Payment completed successfully. "
            "(Demo payment)"
        )


        return redirect(
            "order_success",
            order_id=order.id
        )


    return render(
        request,
        "payments/payment.html",
        {
            "order": order
        }
    )