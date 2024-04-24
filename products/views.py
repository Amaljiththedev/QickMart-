from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import ProductVariant, Products, ProductImage, VariantImage
from category.models import category as Category  # Import the Category model
from category.models import Brand as Brand
from admin_auth import views
from user_profile.models import Order
from decimal import Decimal




# Create your views here.
def product_view(request):
    if "email" in request.session:
        products = Products.objects.all()
        context = {"products": products}
        return render(request, "admin_auth/product_management.html", context)
    return render(request, "admin_auth/authentication-login.html")


def add_product(request):
    if "email" in request.session:
        status_choices = Products.Status_choices  # Use the model's choices
        categories = Category.objects.all()
        brands = Brand.objects.all()

        context = {
            "categories": categories,
            "status_choices": status_choices,
            "brands": brands,
        }

        if request.method == "POST":
            # Retrieve form data
            title = request.POST.get("title")
            category_id = request.POST.get("category")
            description = request.POST.get("description")
            price = Decimal(request.POST.get("price"))
            offer_price = Decimal(request.POST.get("offer_price"))
            brand_id = request.POST.get("brand")
            status = request.POST.get("status")
            stock_count = int(request.POST.get("stock_count"))
            image = request.FILES.get("image")
            weight = Decimal(request.POST.get("weight"))
            height = Decimal(request.POST.get("dimensions"))  # Assuming height corresponds to dimensions
            trending = request.POST.get("trending") == "on"
            product_details = request.POST.get("product_details")

            # Retrieve category and brand objects
            category = Category.objects.get(id=category_id)
            brand = Brand.objects.get(id=brand_id)

            cat_offer = category.category_offer
            product_offer = offer_price

            if cat_offer < product_offer:
                the_offer_price = cat_offer / 100 * price
            else:
                the_offer_price = product_offer / 100 * price

            # Create Products object
            product = Products.objects.create(
                title=title,
                category=category,
                description=description,
                price=price - the_offer_price,
                brand=brand,
                status=status,
                stock_count=stock_count,
                image=image,
                weight=weight,
                height=height,
                trending=trending,
                product_details=product_details,
                offer_price=offer_price,
                actual_price= price # Assign actual_price directly
            )

            print(product.actual_price)
            print(cat_offer)
            print(product_offer)


            if request.FILES.getlist("images"):
                for img in request.FILES.getlist("images"):
                    ProductImage.objects.create(product=product, image=img)

            # Redirect after successful creation
            return redirect("product_management")

        return render(request, "admin_auth/product_add.html", context)
    return render(request, "admin_auth/authentication-login.html")

from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Products, Category, Brand, ProductImage

def update_product(request, id):
    if "email" in request.session:
        # Retrieve the product object to be updated
        product = Products.objects.get(id=id)

        # Retrieve choices and data needed for rendering the form
        status_choices = Products.Status_choices
        categories = Category.objects.all()
        brands = Brand.objects.all()

        context = {
            "categories": categories,
            "status_choices": status_choices,
            "brands": brands,
            "product": product,
        }

        if request.method == "POST":
            # Retrieve form data
            title = request.POST.get("title")
            cat_id = request.POST.get("category")
            description = request.POST.get("description")
            status = request.POST.get("status")
            price = request.POST.get("price")
            brand_id = request.POST.get("brand")
            product_details = request.POST.get("product_details")
            stock_count = request.POST.get("stock_count")
            weight = request.POST.get("weight")
            dimensions = request.POST.get("dimensions")
            trending = request.POST.get("trending") == "on"
            offer_price = request.POST.get("offer_price")

            category = Category.objects.get(id=cat_id)

            cat_offer = Decimal(category.category_offer)
            product_offer = Decimal(offer_price)

            if cat_offer < product_offer:
                the_offer_price = cat_offer / Decimal(100) * Decimal(price)
            else:
                the_offer_price = product_offer / Decimal(100) * Decimal(price)
            # Update product fields
            product.title = title
            product.category = Category.objects.get(id=cat_id)
            product.description = description
            product.price = Decimal(price) - the_offer_price
            product.brand = Brand.objects.get(id=brand_id)
            product.stock_count = stock_count
            product.status = status
            product.weight = weight
            product.height = dimensions
            product.trending = trending
            product.product_details = product_details
            product.offer_price = offer_price
            product.actual_price = price

            print(product.actual_price)
            print(cat_offer)
            print(product_offer)

            # Save the updated product
            product.save()

            # Handle newly uploaded additional images
            new_images = request.FILES.getlist("images")
            for image in new_images:
                ProductImage.objects.create(product=product, image=image)

            # Redirect to the product management page after successful update
            return redirect("product_management")

        # Render the product update form with the context data
        return render(request, "admin_auth/product_update.html", context)


    # If user is not logged in, redirect to the login page
    return render(request, "admin_auth/authentication-login.html")



def block_product(request, id):
    if "email" in request.session:
        product = Products.objects.get(id=id)
        product.is_active = False
        product.save()
        return redirect("product_management")
    return render(request, "admin_auth/authentication-login.html")


def unblock_product(request, id):
    if "email" in request.session:
        product = Products.objects.get(id=id)
        product.is_active = True
        product.save()
        return redirect("product_management")
    return render(request, "admin_auth/authentication-login.html")


def delete_product(request, id):
    if "email" in request.session:
        product = Products.objects.get(id=id)
        product.delete()

        return redirect("product_management")
    return render(request, "admin_auth/authentication-login.html")


def edit_variant(request, variant_id):
    variant_product = get_object_or_404(ProductVariant, id=variant_id)

    if request.method == "POST":
        # Update the variant with the data from the form
        variant_product.size = request.POST.get("size")
        variant_product.color = request.POST.get("color")
        variant_product.price = request.POST.get("price")
        variant_product.stock_count = request.POST.get("stock_count")
        variant_product.save()

        # Handle image uploads
        for image in request.FILES.getlist("images"):
            VariantImage.objects.create(variant=variant_product, image=image)

        # Redirect to the product management page or any other appropriate page
        return redirect("product_management")
    else:
        return render(
            request,
            "admin_auth/edit_variant.html",
            {"variant_product": variant_product},
        )


def delete_variant(request, variant_id):
    variant_product = get_object_or_404(ProductVariant, id=variant_id)
    variant_product.delete()
    return redirect("variant")  # Redirect to product detail page


def block_variant(request, variant_id):
    variant_product = get_object_or_404(ProductVariant, id=variant_id)

    variant_product.is_active = False
    variant_product.save()
    return redirect("variant")  # Redirect to product detail page


def unblock_variant(request, variant_id):
    variant_product = get_object_or_404(ProductVariant, id=variant_id)
    variant_product.is_active = True
    variant_product.save()
    return redirect("variant")


def variant_management(request):
    # Fetch all products from the database
    products = Products.objects.all()
    context = {"products": products}
    return render(request, "admin_auth/variant_management.html", context)


def add_variant(request, product_id):
    if request.method == "POST":
        price = request.POST.get("price")
        stock_count = request.POST.get("stock_count")
        ram = request.POST.get("Ram")
        internal_storage = request.POST.get("internal")
        inch = request.POST.get("inch")
        color = request.POST.get("color")
        images = request.FILES.getlist("images")  # Get list of uploaded images

        # Create a new ProductVariant instance
        variant = ProductVariant(
            product_id=product_id,
            price=price,
            stock_count=stock_count,
            ram=ram,
            internal_storage=internal_storage,
            inch=inch,
            color=color,
        )
        variant.save()

        # Save the uploaded images
        for image in images:
            variant_image = VariantImage(variant=variant, image=image)
            variant_image.save()

        return redirect("variant")  # Redirect to product detail page

    return render(request, "admin_auth/add_variant.html", {"product_id": product_id})


def show_variants(request, product_id):
    product = Products.objects.get(pk=product_id)
    variants = ProductVariant.objects.filter(product_id=product_id)
    return render(
        request,
        "admin_auth/show_variants.html",
        {"product": product, "variants": variants},
    )


def block_variant(request, variant_id):
    variant = ProductVariant.objects.get(pk=variant_id)
    variant.is_active = False
    variant.save()
    return redirect("show_variants")


def delete_variant(request, variant_id):
    variant = get_object_or_404(ProductVariant, pk=variant_id)
    product_id = variant.product_id
    variant.delete()
    return redirect("show_variants", product_id=product_id)
