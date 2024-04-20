from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import ProductVariant, Products, ProductImage, VariantImage
from category.models import category as Category  # Import the Category model
from category.models import Brand as Brand
from admin_auth import views
from user_profile.models import Order


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
            price = request.POST.get("price")
            brand_id = request.POST.get("brand")
            status = request.POST.get("status")
            stock_count = request.POST.get("stock_count")
            image = request.FILES.get("image")
            weight = request.POST.get("weight")
            height = request.POST.get(
                "dimensions"
            )  # Assuming height corresponds to dimensions
            trending = request.POST.get("trending") == "on"
            product_details = request.POST.get("product_details")

            # Retrieve category and brand objects
            category = Category.objects.get(id=category_id)
            brand = Brand.objects.get(id=brand_id)

            # Create Products object
            product = Products.objects.create(
                title=title,
                category=category,
                description=description,
                price=price,
                brand=brand,
                status=status,
                stock_count=stock_count,
                image=image,
                weight=weight,
                height=height,
                trending=trending,
                product_details=product_details,
            )
            if request.FILES.getlist("images"):
                for img in request.FILES.getlist("images"):
                    ProductImage.objects.create(product=product, image=img)

            # Redirect after successful creation
            return redirect("product_management")

        return render(request, "admin_auth/product_add.html", context)
    return render(request, "admin_auth/authentication-login.html")


def update_product(request, id):
    if "email" in request.session:
        product = Products.objects.get(id=id)
        status_choices = Products.Status_choices
        categories = Category.objects.all()
        brand = Brand.objects.all()
        context = {
            "brand": brand,
            "categories": categories,
            "status_choices": status_choices,
            "product": product,
        }
        if request.method == "POST":
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

            # Update product fields
            product.title = title
            product.category = Category.objects.get(id=cat_id)
            product.description = description
            product.price = price
            product.brand = Brand.objects.get(id=brand_id)
            product.stock_count = stock_count
            product.status = status
            product.weight = weight
            product.height = dimensions
            product.trending = trending
            product.product_details = product_details

            # Handle existing additional images
            existing_images = product.additional_images.all()

            # Handle uploaded additional images
            new_images = request.FILES.getlist("images")

            # Save product
            product.save()

            # Save newly uploaded additional images
            for image in new_images:
                ProductImage.objects.create(product=product, image=image)

            return redirect("product_management")

        return render(request, "admin_auth/product_update.html", context)
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
