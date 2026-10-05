from django.shortcuts import get_object_or_404, render

from .models import Product, Category


def home(request):

    products = Product.objects.filter(
        available=True
    ).order_by("-created_at")

    categories = Category.objects.all()

    return render(
        request,
        "store/home.html",
        {
            "products": products,
            "categories": categories,
        }
    )


def product_list(request):

    products = Product.objects.filter(
        available=True
    ).order_by("-created_at")

    categories = Category.objects.all()

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    if search_query:

        products = products.filter(
            name__icontains=search_query
        )


    category_id = request.GET.get(
        "category"
    )

    if category_id:

        products = products.filter(
            category_id=category_id
        )


    return render(
        request,
        "store/products.html",
        {
            "products": products,
            "categories": categories,
            "search_query": search_query,
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product
        }
    )