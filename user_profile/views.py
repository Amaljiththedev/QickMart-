import secrets
import smtplib
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from Qickmart import settings
from category.models import Brand
from inventory.models import Coupon
from products.models import ProductVariant, Products, VariantImage
from registration.views import generate_otp
from user_auth.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Address, Cart, Order, OrderItem, UserWishlist, payment
from django.db.models import Q
from category.models import category as Category
from django.shortcuts import redirect, get_object_or_404
from .models import Cart
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Max
from django.views.decorators.csrf import ensure_csrf_cookie
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle,Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


# Create your views here.
@login_required
def account_page(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    if request.user.is_authenticated:
        custom_user = request.user
        context = {
            "custom_user": custom_user,
        }
        return render(request, "user_auth/account_page.html", context)
    else:
        return render("user_auth/main.html")


@login_required
def manage_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    custom_user = request.user

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        custom_user.first_name = first_name
        custom_user.last_name = last_name
        custom_user.phone = phone
        custom_user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect(
            "user_profile:user_profile_management"
        )  # Redirect to profile page

    context = {"custom_user": custom_user}
    return render(request, "user_auth/profile_manage.html", context)


@login_required
def verify_otp(request):
    context = {"messages": messages.get_messages(request)}

    if request.method == "POST":
        x = request.session.get("otp")
        otp1 = request.POST["otp1"]
        otp2 = request.POST["otp2"]
        otp3 = request.POST["otp3"]
        otp4 = request.POST["otp4"]
        otp5 = request.POST["otp5"]
        otp6 = request.POST["otp6"]

        # Retrieve OTP entered by the user
        entered_otp = (
            str(otp1) + str(otp2) + str(otp3) + str(otp4) + str(otp5) + str(otp6)
        )

        if entered_otp == x:
            # Update the email address in the user's profile
            new_email = request.session.get("new_email")
            request.user.email = new_email
            request.user.save()

            # Clean up session data
            del request.session["new_email"]
            del request.session["otp"]

            messages.success(request, "Email is changed successfully")
            return redirect("account")  # Redirect to profile page
        else:
            messages.error(request, "Invalid OTP")
            return redirect("verify_otp")  # Redirect back to OTP verification page

    return render(request, "registration/verify.html", context)

@login_required
def manage_address(request):
    user = request.user
    addresses = Address.objects.filter(username=user)

    if request.method == "POST":
        house_name = request.POST.get("house_name")
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip")

        # Create a new Address object associated with the current user
        Address.objects.create(
            username=user,
            house_name=house_name,
            street=street,
            city=city,
            state=state,
            zipcode=zip_code,
        )

        # Update the addresses queryset to include the new address
        return redirect("user_profile:manage_address")

    context = {
        "Address": addresses,
    }
    return render(request, "user_auth/manage_address.html", context)

@login_required
def address_edit(request, address_id):
    # Retrieve the existing address object
    address = get_object_or_404(Address, id=address_id)

    if request.method == "POST":
        # Update the fields of the existing address object
        address.house_name = request.POST.get("house_name")
        address.street = request.POST.get("street")
        address.city = request.POST.get("city")
        address.state = request.POST.get("state")
        address.zipcode = request.POST.get("zip")

        # Save the changes
        address.save()

        # Redirect to the manage_address view
        return redirect("user_profile:manage_address")

    # Pass the address object to the template for editing
    context = {
        "address": address,
    }
    return render(request, "user_auth/edit_address.html", context)

@login_required
def view_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    # Pass the address object to the template for viewing
    context = {
        "address": address,
    }
    return render(request, "user_auth/view_address.html", context)

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    address.delete()
    return redirect("user_profile:manage_address")

@login_required
def order_page(request):
    return render(request, "user_auth/orders.html")

@login_required
def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    if request.user.is_authenticated:
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity", 1)



        try:
            product = get_object_or_404(Products, id=product_id)
            wishlist_items = UserWishlist.objects.filter(user=request.user, product=product)
            wishlist_items.delete()


            if product.stock_count <= 0:
                return JsonResponse({"error": "Product is out of stock."}, status=400)

            # Check if requested quantity is available
            if product.stock_count < int(quantity):
                return JsonResponse(
                    {"error": "Insufficient stock available."}, status=400
                )

            cart_item, created = Cart.objects.get_or_create(
                user=request.user, product=product, product_quantity=quantity
            )
            if not created:
                cart_item.product_quantity += int(quantity)
                cart_item.save()

            return JsonResponse({"success": "Item added to cart successfully."})
        except (ValueError, Products.DoesNotExist):
            return JsonResponse(
                {"error": "Invalid product ID or quantity."}, status=400
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "User is not authenticated."}, status=403)

@login_required
def update_cart_quantity(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    try:
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            product_id = request.POST.get("product_id")
            new_quantity = int(request.POST.get("quantity"))

            # Retrieve the product object
            product = get_object_or_404(Products, id=product_id)

            # Get or create the cart item for the user and product
            cart_item, created = Cart.objects.get_or_create(
                user=request.user, product=product
            )

            # Update the cart item quantity
            cart_item.product_quantity = new_quantity
            cart_item.save()

            # Calculate the total price
            total_price = product.price * new_quantity

            # Return JSON response with updated details
            return JsonResponse(
                {
                    "success": "Cart quantity updated successfully",
                    "total_price": total_price,
                }
            )

        else:
            return JsonResponse({"error": "Invalid request"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Invalid quantity value"}, status=400)
    except Exception as e:
        return JsonResponse({"error": "Internal server error."}, status=500)

@login_required
def show_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    # Retrieve the current user's cart items
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.product_quantity for item in cart_items)
    Coupon_discount = 0

    # Calculate stock_count_plus_one for each product in the cart
    max_stock_count_plus_one = Products.objects.aggregate(Max("stock_count"))[
        "stock_count__max"
    ]
    # If there are no products or if the stock count is not available, default to 1
    stock_count_plus_one = max_stock_count_plus_one or 1

    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.discount_type == "percentage":
                Coupon_discount = (total_price * coupon.discount_value) / 100
            elif coupon.discount_type == "fixed_amount":
                Coupon_discount = coupon.discount_value
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code. Please enter a valid coupon code.")

        for item in cart_items:
            item.coupon_discount_amount = Coupon_discount

    # Calculate total price for each cart item
    for item in cart_items:
        item.total_price = (
            item.product.price * item.product_quantity - item.coupon_discount_amount
        )
        item.save()


    # Pass the cart items, total price, and coupon code to the template as context
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "coupon_code": coupon_code if "coupon_code" in locals() else None,
        "stock_count_plus_one": stock_count_plus_one,
    }

    # Pass the cart items to the template
    return render(request, "user_auth/cart.html", context)

@login_required
def cart_items_count(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user).count()
        return JsonResponse({"cart_items_count": cart_items})
    else:
        return JsonResponse({"cart_items_count": 0})


def remove_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    product = cart_item.product

    # Increase the stock count of the product

    cart_item.delete()
    return redirect("user_profile:show_cart")

@login_required
def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    # Retrieve saved addresses from the Address model
    user = request.user
    addresses = Address.objects.filter(username=user)

    # Retrieve payment modes from the payment module
    payment_modes = dict(payment.PAYMENT_CHOICES)

    # Retrieve cart items from the Cart model for the current user
    cart = Cart.objects.filter(user=user)
    total_amount = 0
    # Calculate the total price for each cart item and print quantity of each product
    for item in cart:
        item.total_price = (
            item.product.price * item.product_quantity - item.coupon_discount_amount
        )
        total_amount += item.total_price
    
    context = {
        "addresses": addresses,
        "cart": cart,
        "payment_modes": payment_modes,
        "total_amount": total_amount+50,
    }

    # Render the checkout template with the context
    return render(request, "user_auth/checkoutpage.html", context)

@login_required
def confirm_orders(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    if request.method == "POST":
        # Process form submission
        user = request.user
        address_id = request.POST.get("saved_address")
        payment_method = request.POST.get("payment_method")
        cart = Cart.objects.filter(user=user)
        total_price = sum(
            item.product.price * item.product_quantity - item.coupon_discount_amount
            for item in cart
        )
        payments = request.POST.get("payments")
        order_id = request.POST.get("order_id")

        for item in cart:
            product = item.product
            quantity = item.product_quantity

            product.stock_count -= quantity
            # Update stock count
            product.save()

        if not payment_method:
            payment_method = "unknown"
        # Create the order
        order = Order.objects.create(
            user=user,
            address_id=address_id,
            total_price=total_price,
            payment_method=payment_method,
            razorpay_order_id=order_id,
        )

        # Create order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.product_quantity,
                price=item.product.price * item.product_quantity
                - item.coupon_discount_amount,
            )

        # Clear the cart

        if payment_method == "walletbalance":
            # Redirect to wallet_payment with order_id
            return redirect("user_profile:wallet_payment", order_id=order.id)

        messages.success(request, "Order placed successfully.")
        return redirect("user_profile:order_confirmation", order_id=order.id)
    else:
        # Display the checkout page with the form
        user = request.user
        addresses = Address.objects.filter(username=user)
        cart_items = Cart.objects.filter(user=user)
        payment_modes = dict(payment.PAYMENT_CHOICES)
        total = sum(item.product.price * item.product_quantity for item in cart_items)

        context = {
            "addresses": addresses,
            "cart_items": cart_items,
            "payment_modes": payment_modes,
            "total": total,
        }
        return render(request, "user_auth/confirm_orders.html", context)

@login_required
def order_confirmation(request, order_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all()
    cart = Cart.objects.filter(user=request.user)  # Fetch related OrderItem objects
    cart.delete()
    context = {
        "order": order,
        "order_items": order_items,  # Pass the order items to the template
    }
    return render(request, "user_auth/orderconfirmed.html", context)

@login_required
def user_orders(request):
    # Fetch orders related to the current user
    user_orders = Order.objects.filter(user=request.user)

    context = {
        "orders": user_orders,
    }
    return render(request, "user_auth/user_orders.html", context)

@login_required
def cancel_order(request, order_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    order = get_object_or_404(Order, id=order_id)

    if order.status != "Shipped":
        # Cancel the order
        order.status = "Cancelled"
        order.save()

        # Update product stock_count for each OrderItem in the order
        for order_item in order.orderitem_set.all():
            product = order_item.product
            product.stock_count += order_item.quantity
            product.save()

        return redirect("user_profile:user_orders")
    else:
        # Handle error or redirect to appropriate page
        return redirect("some_error_page")

@login_required
def track_order(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    # Retrieve orders for the logged-in user
    user = request.user  # Assuming you're using Django's built-in authentication system
    orders = Order.objects.filter(user=user)

    context = {
        "orders": orders,
    }
    return render(request, "user_auth/track_order.html", context)


@login_required
def wallet_payment(request, order_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access wallet payment.")
        return redirect("login")
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()
    user_profile = request.user
    cart = Cart.objects.filter(user=user_profile)

    if request.method == "POST":
        wallet_balance = user_profile.wallet_balance
        total_price = order.total_price

        for item in cart:
            product = item.product
            quantity = item.product_quantity

            product.stock_count -= quantity
            # Update stock count
            product.save()


        if wallet_balance >= total_price > 0:
            with transaction.atomic():
                user_profile.wallet_balance -= total_price
                user_profile.save()
                order.paid = True
                order.save()
                Cart.objects.filter(user=request.user).delete()
                messages.success(request, "Payment successful. Order placed.")
                return redirect("user_profile:order_confirmation", order_id=order.id)
        else:
            order.paid = False
            order.status = "Payment pending" 
            order.save()
            messages.error(request, "Insufficient funds in wallet. Payment failed.")
            return redirect("user_profile:wallet_payment", order_id=order.id)

    context = {
        "order": order,
        "order_items": order_items,
        "wallet_balance": user_profile.wallet_balance,
    }
    return render(request, "user_auth/wallet_payment.html", context)




@login_required
def wishlist(request):
    wishlist_items = UserWishlist.objects.filter(user=request.user)

    context = {"wishlist_items": wishlist_items}
    return render(request, "user_auth/wishlist.html", context)

@login_required
def user_add_to_wishlist(request):
    if request.method == "POST" and request.user.is_authenticated:
        product_id = request.POST.get("product_id")

        product = get_object_or_404(Products, id=product_id)

        # Check if the product is already in the user's wishlist
        if UserWishlist.objects.filter(user=request.user, product=product).exists():
            return JsonResponse(
                {"error": "Product is already in the wishlist."}, status=400
            )

        # Create a new UserWishlist object for the user and product
        UserWishlist.objects.create(user=request.user, product=product)

        return JsonResponse({"success": "Product added to wishlist successfully."})

    return JsonResponse(
        {"error": "User is not authenticated or request method is not POST."},
        status=403,
    )

@login_required
def remove_from_wishlist(request, id):
    item = get_object_or_404(UserWishlist, id=id)

    item.delete()
    return redirect("user_profile:wishlist")


@login_required
def razor_payment(request):
    payments = request.GET.get(
        "payments"
    ) 
    order_id = request.GET.get(
        "order_id"
    ) 


    context = {"order_id": order_id}


    return render(request, "user_auth/razor_payment.html", context)

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if not order.paid and order.payment_method != "Cash on Delivery":
        # If payment for the order has failed and it's not COD, render a different template
        return render(request, "user_auth/failed_order.html")

    tracking_steps = [
        {"icon": "fa fa-check", "text": "Order confirmed", "active": False},
        {"icon": "fa fa-user", "text": "Picked by courier", "active": False},
        {"icon": "fa fa-truck", "text": "Out_of_delivery", "active": False},
    ]

    if order.status == "Pending":
        tracking_steps[0]["active"] = True
    elif order.status == "Processing":
        tracking_steps[0]["active"] = True
    elif order.status == "Shipped":
        tracking_steps[0]["active"] = True
        tracking_steps[1]["active"] = True
    elif order.status == "Out of delivery":
        tracking_steps[0]["active"] = True
        tracking_steps[1]["active"] = True
        tracking_steps[2]["active"] = True

    context = {"order": order, "tracking_steps": tracking_steps}
    return render(request, "user_auth/track_order.html", context)

@login_required
def reset_password(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("forget_password")
    else:
        messages.info(request, 'Please log in to access this page.')
        return render(request, "user_auth/reset_password.html")

@csrf_exempt
@login_required
def razorpay_callback(request):
    if request.method == "POST":
        data = request.POST
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(cart_item.product.price for cart_item in cart_items)
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_price=total_price,
                    payment_method="Razorpay",
                    paid=True,  # Assume payment is successful initially
                    razorpay_order_id=data.get('razorpay_payment_id'),
                )
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.product_quantity,
                        price=cart_item.product.price,
                    )
            for item in cart_items:
                product = item.product
                quantity = item.product_quantity
                product.stock_count -= quantity
                
            # Update stock count
                product.save()
            cart_items.delete()
            return render(
                request,
                "user_auth/success.html",
            )
        except Exception as e:
            if order:
                order.paid = False 
                order.status="Payment pending"
                order.save()
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Only POST method is allowed"}, status=405
        )
@login_required
def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    template_path = 'user_auth/pdf.html'
    context = {'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


@login_required
@ensure_csrf_cookie
def variant_add_to_cart(request):
    if request.method == "POST":
        # Retrieve data from the POST request
        product_id = request.POST.get("product_id")
        variant_id = request.POST.get("variant_id")
        quantity = request.POST.get("quantity", 1)

        # Check if product_id and variant_id are provided
        if not product_id or not variant_id:
            return JsonResponse({"error": "Product ID or Variant ID is missing."}, status=400)

        # Retrieve the variant and product objects
        variant = get_object_or_404(ProductVariant, id=variant_id)
        product = variant.product

        # Retrieve the variant image
        variant_image = VariantImage.objects.filter(variant=variant).first()

        # Create or update the cart item
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product, variant=variant
        )
        # Update product quantity
        cart_item.product_quantity = int(quantity)
        # Update price and image of the cart item
        cart_item.price = variant.price
        if variant_image:
            cart_item.image = variant_image.image
        cart_item.save()

        return JsonResponse({"success": "Variant added to cart successfully."})
    else:
        # Return error for non-POST requests
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
