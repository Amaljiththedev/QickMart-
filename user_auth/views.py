from decimal import Decimal
from django.shortcuts import render
from category.models import category, Brand
from banner.models import Banner
from category.views import views
from products.models import ProductVariant, Products, ProductImage
import os
from django.db.models import Q, Count
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse


# Create your views here.
def base(request):
    return render(request, "user_auth/base.html")


def home(request):
    Category = category.objects.filter(is_active=True)[:5]
    products = Products.objects.filter(is_active=True, status="In Stock")
    brand = Brand.objects.all()
    allban = Banner.objects.all()

    context = {
        "Category": Category,
        "products": products,
        "brand": brand,
        "allban": allban,
    }

    return render(request, "user_auth/main.html", context)


def user_product_view(request, id):
    product = Products.objects.get(id=id)
    product_images = ProductImage.objects.filter(product=product)
    variants = ProductVariant.objects.filter(product=product)
    product = Products.objects.get(id=id)
    similar_products = Products.objects.filter(category=product.category).exclude(
        id=product.id
    )

    context = {
        "product_images": product_images,
        "product": product,
        "variants": variants,
        "similar_products": similar_products,
    }

    return render(request, "user_auth/product-view.html", context)


def banner_view(request):
    laptop_banner = category.objects.get(name="Laptop")
    Tvandbanner = category.objects.get(name="Tv and audio")
    smartphonebanner = category.objects.get(name="smartphone")
    wearablesbanner = category.objects.get(name="Wearables")

    allban = Banner.objects.filter(is_active=True)
    lapban = Banner.objects.filter(category=laptop_banner, is_active=True)
    tvban = Banner.objects.filter(category=Tvandbanner, is_active=True)
    smartphoneban = Banner.objects.filter(category=smartphonebanner, is_active=True)
    wearablesbanner = Banner.objects.filter(category=wearablesbanner, is_active=True)

    context = {
        "allban": allban,
        "lapban": lapban,
        "tvban": tvban,
        "wearablesbanner": wearablesbanner,
        "smartphoneban": smartphoneban,
    }

    return render(request, "user_auth/main.html", context)


def list_of_products(request):
    products = Products.objects.filter(is_active=True)
    categories = category.objects.all()
    brand = Brand.objects.all()
    category_id = request.GET.get("category")
    brand_id = request.GET.get("brand")
    sort_by = request.GET.get("sort_by")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price is not None and max_price is not None:
        products = products.filter(price__range=(min_price, max_price))

    if category_id:
        products = products.filter(category_id=category_id)
    elif brand_id:
        products = products.filter(brand_id=brand_id)
    elif sort_by:
        if sort_by == "sales_asc":
            products = products.order_by("title")  # Sort by product name ascending
        elif sort_by == "sales_desc":
            products = products.order_by("-title")  # Sort by product name descending
        elif sort_by == "price_asc":
            products = products.order_by("price")  # Sort by price ascending
        elif sort_by == "rating_asc":
            products = products.order_by("rating")  # Sort by rating ascending
        elif sort_by == "date_desc":
            products = products.order_by(
                "-created_date"
            )  # Sort by creation date descending

        elif sort_by == "trending":
            products = products.annotate(num_orders=Count("order")).order_by(
                "-num_orders"
            )

        elif sort_by == "featured":
            products = products.filter(trending=True)
    context = {
        "products": products,
        "categories": categories,
        "brand": brand,
        "sort_by": sort_by,
        "min_price": min_price,
        "max_price": max_price,
        # Pass the current sorting parameter to the template
    }

    return render(request, "user_auth/product_list.html", context)


def search(request):
    query = (
        request.POST.get("searched")
        or request.GET.get("searched")
        or request.session.get("searched_query", "")
    )
    request.session["searched_query"] = query
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    category_id = request.GET.get("category_id")
    brand_id = request.GET.get("brand_id")

    products = Products.objects.all()

    # Filter products based on the search query
    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(category__name__icontains=query)
            | Q(brand__brand_name__icontains=query)
        )

    # Filter products based on the price range
    if min_price is not None and max_price is not None:
        min_price = Decimal(min_price)
        max_price = Decimal(max_price)
        products = products.filter(price__range=(min_price, max_price))

    # Filter products based on the category
    if category_id:
        products = products.filter(category_id=category_id)

    # Filter products based on the brand
    if brand_id:
        products = products.filter(brand_id=brand_id)

    categories = category.objects.all()
    brands = Brand.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "brands": brands,
        "searched_query": query,
        "selected_category": int(category_id) if category_id else None,
        "selected_brand": int(brand_id) if brand_id else None,
    }

    return render(request, "user_auth/search.html", context)


def get_variant_details(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    # You can customize the data you want to return here
    variant_data = {
        "id": variant.id,
        "price": variant.price,
        "ram": variant.ram,
        "internal_storage": variant.internal_storage,
        "inch": variant.inch,
        "color": variant.color,
    }
    return render(request, "user_auth/variant_details.html", {"variant": variant})
