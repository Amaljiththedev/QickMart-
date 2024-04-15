import secrets
import smtplib
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from Qickmart import settings
from category.models import Brand
from inventory.models import Coupon
from products.models import Products
from registration.views import generate_otp
from user_auth.models import CustomUser 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Address, Cart, Order, OrderItem, UserWishlist, payment,Wishlist
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




import razorpay
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_SECRET_KEY))



# Create your views here.
@login_required 
def account_page(request):
    if request.user.is_authenticated:
        custom_user = request.user
        context = {
            'custom_user': custom_user,
        }
        return render(request, 'user_auth/account_page.html', context)
    else:
        return render('user_auth/main.html')
@login_required    
def manage_profile(request):
    custom_user = request.user
    
    if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            custom_user.first_name = first_name
            custom_user.last_name = last_name
            custom_user.phone = phone
            custom_user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile:user_profile_management')  # Redirect to profile page

    context = {'custom_user': custom_user}
    return render(request, 'user_auth/profile_manage.html', context)

@login_required
def verify_otp(request):
    context = {
        'messages': messages.get_messages(request)
    }
    
    if request.method == "POST":
        x = request.session.get('otp')
        otp1       =  request.POST['otp1']
        otp2=request.POST['otp2']
        otp3=request.POST['otp3']
        otp4=request.POST['otp4']
        otp5=request.POST['otp5']
        otp6=request.POST['otp6']    
       
        # Retrieve OTP entered by the user
        entered_otp =(str(otp1)+str(otp2)+str(otp3)+str(otp4)+str(otp5)+str(otp6))
        
        if entered_otp == x:
            # Update the email address in the user's profile
            new_email = request.session.get('new_email')
            request.user.email = new_email
            request.user.save()
            
            # Clean up session data
            del request.session['new_email'] 
            del request.session['otp']       
            
            messages.success(request, "Email is changed successfully")
            return redirect('account')  # Redirect to profile page
        else:
            messages.error(request, "Invalid OTP")
            return redirect('verify_otp')  # Redirect back to OTP verification page

    return render(request, 'registration/verify.html', context)



def manage_address(request):
    user = request.user
    addresses = Address.objects.filter(username=user)

    if request.method == "POST":
        house_name = request.POST.get('house_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

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
        return redirect('user_profile:manage_address')

    context = {
        'Address': addresses,
    }
    return render(request, 'user_auth/manage_address.html', context)


def address_edit(request, address_id):
    # Retrieve the existing address object
    address = get_object_or_404(Address, id=address_id)

    if request.method == "POST":
        # Update the fields of the existing address object
        address.house_name = request.POST.get('house_name')
        address.street = request.POST.get('street')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.zipcode = request.POST.get('zip')

        # Save the changes
        address.save()

        # Redirect to the manage_address view
        return redirect('user_profile:manage_address')

    # Pass the address object to the template for editing
    context = {
        'address': address,
    }
    return render(request, 'user_auth/edit_address.html', context)
    
def view_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    # Pass the address object to the template for viewing
    context = {
        'address': address,
    }
    return render(request, 'user_auth/view_address.html', context)

def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    address.delete()
    return redirect('user_profile:manage_address')
    
    
def order_page(request):
    return render(request, 'user_auth/orders.html')


def add_to_cart(request):
    if request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity',1)

        try:
            product = get_object_or_404(Products, id=product_id)
            
            if product.stock_count <= 0:
                return JsonResponse({'error': 'Product is out of stock.'}, status=400)

            # Check if requested quantity is available
            if product.stock_count < int(quantity):
                return JsonResponse({'error': 'Insufficient stock available.'}, status=400)

            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product,product_quantity=quantity)
            if not created:
                cart_item.product_quantity += int(quantity)
                cart_item.save()
            print(cart_item.product.price)

            # Update the stock count of the product


            return JsonResponse({'success': 'Item added to cart successfully.'})
        except (ValueError, Products.DoesNotExist):
            return JsonResponse({'error': 'Invalid product ID or quantity.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=403)
    


def update_cart_quantity(request):
    try:
        print("Received AJAX request to update cart quantity")
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            product_id = request.POST.get('product_id')
            new_quantity = int(request.POST.get('quantity'))
            print(F'THIS IS NEW QUANTITY', new_quantity)

            cart_item = get_object_or_404(Cart, product_id=product_id)

            # Calculate the difference between the new quantity and the existing quantity in the cart
            quantity_diff = new_quantity - cart_item.product_quantity
            cart_item.product_quantity = new_quantity
            cart_item.save()
            if quantity_diff > cart_item.product.stock_count:
                return JsonResponse({'error': 'Requested quantity exceeds available stock count.'}, status=400)

            # Update the stock count
            # remaining_stock = cart_item.product.stock_count - quantity_diff
            # print(F'THIS IS REMAINING', remaining_stock)
            # cart_item.product.stock_count = remaining_stock
            # cart_item.product.save()

            # Update the cart item quantity
            # cart_item.product_quantity = new_quantity
            # print(F'UPDATED QUANTITY', cart_item.product_quantity)
            # cart_item.save()

            # Calculate the total price
            total_price = cart_item.product.price * new_quantity

            return JsonResponse({'success': 'Cart quantity updated successfully', 'total_price': total_price, 'remaining_stock': remaining_stock})
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Internal server error.'}, status=500)

def show_cart(request):
    # Retrieve the current user's cart items
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.product_quantity for item in cart_items)

    Coupon_discount = 0

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            print("Coupon information:", coupon.code, coupon.discount_type, coupon.discount_value)  # Debug coupon information
            if coupon.discount_type == 'percentage':
                Coupon_discount = (total_price * coupon.discount_value) / 100
                print(Coupon_discount)
            elif coupon.discount_type == 'fixed_amount':
                Coupon_discount = coupon.discount_value
                print(total_price)
        except Coupon.DoesNotExist:
            print("Coupon not found")
            pass  # Handle invalid coupon code here

        for item in cart_items:
            item.coupon_discount_amount = Coupon_discount

    # Calculate total price for each cart item
    for item in cart_items:
        item.total_price = item.product.price * item.product_quantity - item.coupon_discount_amount
        item.save()

    print(total_price)

    # Pass the cart items, total price, and coupon code to the template as context
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'coupon_code': coupon_code if 'coupon_code' in locals() else None,
    }

    # Pass the cart items to the template
    return render(request, 'user_auth/cart.html', context)




def cart_items_count(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user).count()
        return JsonResponse({'cart_items_count': cart_items})
    else:
        return JsonResponse({'cart_items_count': 0})
    
    


def remove_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    product = cart_item.product

    # Increase the stock count of the product

    cart_item.delete()
    return redirect('user_profile:show_cart')


def checkout(request):
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
            item.total_price = item.product.price * item.product_quantity - item.coupon_discount_amount
            total_amount += item.total_price
            print(item.coupon_discount_amount)
            print(f"Product:, Quantity: {item.product_quantity}")
        
        context = {
            'addresses': addresses,
            'cart': cart,
            'payment_modes': payment_modes,
            'total_amount': total_amount,
        }
        
        # Render the checkout template with the context
        return render(request, 'user_auth/checkoutpage.html', context)


def confirm_orders(request):
    if request.method == 'POST':
        # Process form submission
        user = request.user
        address_id = request.POST.get('saved_address')
        payment_method = request.POST.get('payment_method')
        cart = Cart.objects.filter(user=user)
        total_price = sum(item.product.price * item.product_quantity - item.coupon_discount_amount for item in cart)
        print(total_price)
        payments = request.POST.get('payments')
        order_id = request.POST.get('order_id')



        for item in cart:
            product = item.product
            quantity = item.product_quantity

            # Update stock count
            product.stock_count -= quantity
            product.save()

        if not payment_method:
            payment_method = 'unknown'
        # Create the order
        order = Order.objects.create(
            user=user,
            address_id=address_id,
            total_price=total_price,
            payment_method=payment_method,
            razorpay_order_id=order_id
        )

        # Create order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.product_quantity,
                price=item.product.price * item.product_quantity - item.coupon_discount_amount

            )

        # Clear the cart


        


        if payment_method == 'walletbalance':
            # Redirect to wallet_payment with order_id
            return redirect('user_profile:wallet_payment', order_id=order.id)


        messages.success(request, 'Order placed successfully.')
        return redirect('user_profile:order_confirmation', order_id=order.id)
    else:
        # Display the checkout page with the form
        user = request.user
        addresses = Address.objects.filter(username=user)
        cart_items = Cart.objects.filter(user=user)
        payment_modes = dict(payment.PAYMENT_CHOICES)
        total = sum(item.product.price * item.product_quantity for item in cart_items)

        context = {
            'addresses': addresses,
            'cart_items': cart_items,
            'payment_modes': payment_modes,
            'total': total,
        }
        return render(request, 'user_auth/confirm_orders.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all() 
    cart = Cart.objects.filter(user=user) # Fetch related OrderItem objects
    cart.delete()
    context = {
        'order': order,
        'order_items': order_items,  # Pass the order items to the template
    }
    return render(request, 'user_auth/orderconfirmed.html', context)


def user_orders(request):
    # Fetch orders related to the current user
    user_orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': user_orders,
    }
    return render(request, 'user_auth/user_orders.html', context)


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.status != 'Shipped':
        # Cancel the order
        order.status = 'Cancelled'
        order.save()
        
        # Update product stock_count for each OrderItem in the order
        for order_item in order.orderitem_set.all():
            product = order_item.product
            product.stock_count += order_item.quantity
            product.save()
        
        return redirect('user_profile:user_orders')
    else:
        # Handle error or redirect to appropriate page
        return redirect('some_error_page')


def track_order(request):
    # Retrieve orders for the logged-in user
    user = request.user  # Assuming you're using Django's built-in authentication system
    orders = Order.objects.filter(user=user)

    
    context = {
        'orders': orders,
    }
    return render(request, 'user_auth/track_order.html', context)

def wallet_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all()
    cart = Cart.objects.filter(user=request.user)
 # Fetch related OrderItem objects
    

    user_profile = request.user  # Assuming user profile is associated with the user

    if request.method == 'POST':
        wallet_balance = user_profile.wallet_balance
        total_price = order.total_price 

        for x in cart:
            total_price -= x.coupon_discount_amount

        if wallet_balance >= total_price and wallet_balance > 0:
            user_profile.wallet_balance -= total_price
            user_profile.save()
            order.paid = True
            order.save()
            messages.success(request, 'Payment successful. Order placed.')
            return redirect('user_profile:order_confirmation', order_id=order.id)
        else:
            messages.error(request, 'Insufficient funds in wallet.')
            return redirect('user_profile:wallet_payment', order_id=order.id)
    cart.delete()
    context = {
        'order': order,
        'order_items': order_items,
        'wallet_balance': user_profile.wallet_balance,
    }
    return render(request, 'user_auth/wallet_payment.html', context)



def wishlist(request):
    wishlist_items = UserWishlist.objects.filter(user=request.user)
    
    context={
        'wishlist_items':wishlist_items
    }
    return render(request, 'user_auth/wishlist.html',context)


def user_add_to_wishlist(request):
    if request.method == 'POST' and request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        
        product = get_object_or_404(Products, id=product_id)
        
        # Check if the product is already in the user's wishlist
        if UserWishlist.objects.filter(user=request.user, product=product).exists():
            return JsonResponse({'error': 'Product is already in the wishlist.'}, status=400)

        # Create a new UserWishlist object for the user and product
        UserWishlist.objects.create(user=request.user, product=product)

        return JsonResponse({'success': 'Product added to wishlist successfully.'})
    
    return JsonResponse({'error': 'User is not authenticated or request method is not POST.'}, status=403)


def remove_from_wishlist(request,id):
    item=get_object_or_404(UserWishlist,id=id)
    
    item.delete()
    return redirect('user_profile:wishlist')

def success(request):

    if request.method=='POST':
        a=request.POST
        order_id =""
        

        for key,val in a.items():
            if key== "razor_order_id":
                order_id=val
                break

        user=Order.objects,filter(razorpay_order_id_id=order_id).first()
        user.paid=True
        user.save()
        print('hheellllooooo')

    return render(request,'user_auth/success.html')




def razor_payment(request):
    payments = request.GET.get('payments')  # Get the value of 'payments' query parameter
    order_id = request.GET.get('order_id')  # Get the value of 'order_id' query parameter
    print(f'hi this is order_id', order_id)
    
    context = {
        "order_id": order_id
    }

    # Now you can use the 'payments' and 'order_id' variables as needed
    # For example, you can pass them to the template context to render them in the HTML template
    
    return render(request, "user_auth/razor_payment.html", context)


def order_details(request, order_id):
    order = Order.objects.get(id=order_id)  # Assuming you have a model named Order

    tracking_steps = [
        {"icon": "fa fa-check", "text": "Order confirmed", "active": False},
        {"icon": "fa fa-user", "text": "Picked by courier", "active": False},
        {"icon": "fa fa-truck", "text": "Out_of_delivery", "active": False},
    ]

    if order.status == 'Pending':
        tracking_steps[0]['active'] = True
    elif order.status == 'Processing':
        tracking_steps[0]['active'] = True
    elif order.status == 'Shipped':
        tracking_steps[0]['active'] = True
        tracking_steps[1]['active'] = True
    elif order.status == 'Out of delivery':
        tracking_steps[0]['active'] = True
        tracking_steps[1]['active'] = True
        tracking_steps[2]['active'] = True

    context = {
        'order': order,
        'tracking_steps':tracking_steps
    }
    return render(request, 'user_auth/track_order.html', context)


def reset_password(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('forget_password')
    


@csrf_exempt
def razorpay_callback(request):
    if request.method == 'POST':
        # Process the callback data from Razorpay
        data = request.POST  
        print(data)
        
        # Retrieve cart items for the current user
        cart_items = Cart.objects.filter(user=request.user)
        
        # Calculate total price based on cart items
        total_price = sum(cart_item.product.price for cart_item in cart_items)
        
        # Create a new order object with the total price
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                payment_method='Razorpay', # Assuming Razorpay is the payment method
                paid=True
            )
            
            # Create order items for each cart item
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.product_quantity,
                    price=cart_item.product.price
                    # Add other relevant fields
                )
        
        # Clear the cart after creating the order
        cart_items.delete()
        
        # Return a JSON response indicating successful processing of the callback
        return render(request, 'user_auth/success.html',)
    else:
        # Return a 405 Method Not Allowed response for other HTTP methods
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)
