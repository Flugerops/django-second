from django.shortcuts import render, get_object_or_404

from .models import Product, Category


# Create your views here.


def index(request):
    products = Product.objects.all()
    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")

    categories = Category.objects.all()

    if category_name:
        category = Category.objects.get(name=category_name)
        products = products.filter(category=category)

    match filter_name:
        case "price_increase":
            products = products.order_by("price")
        case "price_decrease":
            products = products.order_by("-price")
        case "rating_increase":
            products = products.order_by("rating")
        case "rating_decrease":
            products = products.order_by("-rating")

    return render(
        request, "index.html", context={"products": products, "categories": categories}
    )


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_details.html", {"product": product})
