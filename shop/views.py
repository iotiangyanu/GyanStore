from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from . models import Category, Product, Review
# Create your views here.
def index(request):
    return render(request, 'shop/index.html')

def shop_home(request):
    query = request.GET.get("q")
    category_slug = request.GET.get("category")

    products_queryset = Product.objects.filter(is_active=True)

    if query:
        products_queryset = products_queryset.filter(name__icontains=query)

    if category_slug:
        products_queryset = products_queryset.filter(category__slug=category_slug)

    categories = Category.objects.prefetch_related(
        Prefetch(
            "products",
            queryset=products_queryset,
            to_attr="filtered_products"
        )
    )

    context = {
        "categories": categories,
        "products": products_queryset,
    }

    return render(request, "shop/index.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by("-created_at")

    return render(request, "shop/product_detail.html", {
        "product": product,
        "reviews": reviews,
    })


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    return redirect("product_detail", slug=slug)
