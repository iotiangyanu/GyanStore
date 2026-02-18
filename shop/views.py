from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Prefetch, Avg, Count, FloatField, Q
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from . models import Category, Product, Review
# Create your views here.

def index(request):
    return render(request, 'shop/index.html')

def shop_home(request):
    query = request.GET.get("q")
    category_slug = request.GET.get("category")

    # Base queryset for products
    products_queryset = Product.objects.filter(is_active=True, status='approved').annotate(
        avg_rating=Coalesce(
            Avg("reviews__rating", output_field=FloatField()),
            0.0
        ),
        total_reviews=Count("reviews")
    )

    # Apply search filter
    if query:
        products_queryset = products_queryset.filter(name__icontains=query)

    # Apply category filter
    if category_slug:
        products_queryset = products_queryset.filter(category__slug=category_slug)

    # Always show all categories in dropdown
    all_categories = Category.objects.all().order_by('name')

    # For display, determine which categories to show
    if category_slug:
        # If a specific category is selected, show only that category with its products
        categories_to_display = Category.objects.filter(
            slug=category_slug
        ).prefetch_related(
            Prefetch(
                "products",
                queryset=products_queryset,
                to_attr="filtered_products"
            )
        )
    else:
        # If no category filter, show categories with matching products
        category_ids = products_queryset.values_list('category_id', flat=True).distinct()
        categories_to_display = Category.objects.filter(
            id__in=category_ids
        ).prefetch_related(
            Prefetch(
                "products",
                queryset=products_queryset,
                to_attr="filtered_products"
            )
        ).order_by('name')

    context = {
        "all_categories": all_categories,  # For dropdown
        "categories": categories_to_display,  # For display
        "products": products_queryset,
    }

    return render(request, "shop/index.html", context)


def product_detail(request, slug):
    identifier = slug
    product = None

    # Try slug first, then fall back to numeric id if slug lookup fails
    try:
        product = Product.objects.get(slug=identifier, status='approved')
    except Product.DoesNotExist:
        if identifier.isdigit():
            product = get_object_or_404(Product, id=int(identifier), status='approved')
        else:
            raise

    reviews = product.reviews.all().order_by("-created_at")

    return render(request, "shop/product_detail.html", {
        "product": product,
        "reviews": reviews,
    })


@login_required
def add_review(request, slug):
    identifier = slug

    # flexible lookup: slug or numeric id
    try:
        product = Product.objects.get(slug=identifier)
    except Product.DoesNotExist:
        if identifier.isdigit():
            product = get_object_or_404(Product, id=int(identifier))
        else:
            raise

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    # Redirect to canonical slug URL
    return redirect("product_detail", slug=product.slug)



