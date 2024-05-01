from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

import products
from user_profile.models import Order
from .models import Coupon, Stock
from products.models import Products

# View for Managing Stock
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def stock_management(request):
    if "email" in request.session:
        stock_items = Products.objects.all()

        context = {"stock_items": stock_items}

        return render(request, "admin_auth/inventory.html", context)
    return render(request, "admin_auth/authentication-login.html")


# View for Updating Stock
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_stock(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity", 0)

        # Ensure product_id is provided
        if not product_id:
            return HttpResponse("Product ID is missing", status=400)

        # Validate product_id
        try:
            product = Products.objects.get(pk=product_id)
        except Products.DoesNotExist:
            return HttpResponse("Product not found", status=404)
        else:
            # Validate quantity
            try:
                quantity = int(quantity)
            except ValueError:
                return HttpResponse("Invalid quantity", status=400)

            # Update stock count
            product.stock_count = quantity
            product.save()

            return redirect(
                "stock_management"
            )  # Redirect to the inventory page after successful update

        # Return an HttpResponse with an error message if accessed via GET or any other method
        return HttpResponse("Method not allowed", status=405)
    return render(request, "admin_auth/authentication-login.html")


# Order Management Views
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def order_management(request):
    if "email" in request.session:
        if request.method == "POST":
            order_id = request.POST.get("order_id")
            new_status = request.POST.get("new_status")

            try:
                order = Order.objects.get(pk=order_id)
                order.status = new_status
                order.save()
                return JsonResponse(
                    {"success": True, "message": "Status updated successfully"}
                )
            except Order.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Order not found"}, status=404
                )

        else:
            # If it's a GET request, fetch orders and render the template
            orders = Order.objects.all()
            return render(
                request, "admin_auth/order_management.html", {"orders": orders}
            )
    return render(request, "admin_auth/authentication-login.html")
# View for Updating Order Status
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_status(request, order_id):
    if "email" in request.session:
        order = get_object_or_404(Order, id=order_id)
        if request.method == "POST":
            new_status = request.POST.get("new_status")
            order.status = new_status
            order.save()
        # Redirect back to the same page after updating status
        return redirect("order_management")
    return render(request, "admin_auth/authentication-login.html")


# View for Updating Order Status
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        # Update order details based on admin input
        order.estimated_delivery_time = request.POST.get("estimated_delivery_time")
        order.tracking_number = request.POST.get("tracking_number")
        order.save()
        return redirect("order_management")
    # Render the custom HTML form for updating order details
    return render(request, "admin_auth/update_order_details.html", {"order": order})



# View for Refunding Order
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def refund_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Add total price to user's wallet balance
    order.user.wallet_balance += order.total_price
    order.user.save()
    # Update order status to reflect refund
    order.status = "Refunded"
    order.save()

    for order_item in order.orderitem_set.all():
        product = order_item.product
        product.stock_count += order_item.quantity
        product.save()

        # Redirect to order management page or any other appropriate page
    return redirect("order_management")

# Coupon Management Views
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def coupon_list(request):
    coupons = Coupon.objects.all()

    context = {"coupons": coupons}

    return render(request, "admin_auth/coupon_management.html", context)

# View for Adding Coupon
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def add_coupon(request):
    if request.method == "POST":
        code = request.POST.get("code")
        discount_type = request.POST.get("discount_type")
        discount_value = request.POST.get("discount_value")
        min_order_value = request.POST.get("min_order_value")
        expiration_date = request.POST.get("expiration_date")
        max_uses = request.POST.get("max_uses")

        # Validate and save the coupon (You might want to add more validation logic here)
        if (
            code
            and discount_type
            and discount_value
            and min_order_value
            and expiration_date
            and max_uses
        ):
            Coupon.objects.create(
                code=code,
                discount_type=discount_type,
                discount_value=discount_value,
                min_order_value=min_order_value,
                expiration_date=expiration_date,
                max_uses=max_uses,
            )
            return redirect("coupon_management")
    return render(request, "admin_auth/add_coupon.html")


# View for Deleting Coupon
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    context = {
        "coupon": coupon,
    }
    coupon.delete()
    return redirect("coupon_management")


# View for Deleting Coupon
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    context = {
        "coupon": coupon,
    }
    if request.method == "POST":
        # Update the coupon with the new data from the form
        coupon.code = request.POST.get("code")
        coupon.discount_type = request.POST.get("discount_type")
        coupon.discount_value = request.POST.get("discount_value")
        coupon.min_order_value = request.POST.get("min_order_value")
        coupon.expiration_date = request.POST.get("expiration_date")
        coupon.max_uses = request.POST.get("max_uses")
        coupon.save()
        return redirect("coupon_list")  # Redirect to the coupon list page after editing
    return render(request, "admin_auth/edit_coupon.html", context)
