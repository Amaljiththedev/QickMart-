from django.utils import timezone
from django.db import models
from user_auth.models import CustomUser
from products.models import Products
# Create your models here.
class Address(models.Model):
    username = models.ForeignKey(CustomUser, related_name='user_name', on_delete=models.CASCADE)
    house_name=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    

class Cart(models.Model):
    
    user=models.ForeignKey(CustomUser, related_name='customername', on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=True)
    product_quantity=models.IntegerField(default=1, null=True,blank=False)
    created_date=models.DateField(default=timezone.now)
    coupon_discount_amount=models.IntegerField(default=0, null=True, blank=False)
    
class payment(models.Model):
    PAYMENT_CHOICES = [
        ('Cash on delivery', 'Cash on delivery'),
        ('Razor Pay', 'Razor Pay'),
        ('walletbalance', 'Wallet Balance'),
    ]
    user=models.ForeignKey(CustomUser, related_name='customer', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, null=True, blank=True)




class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Out of delivery', 'Out of delivery'),
        ('Return', 'Return'),
        ('Refunded', 'Refunded'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through='OrderItem')
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    estimated_delivery_time=models.DateField(null=True, blank=True)
    tracking_number=models.CharField(max_length=10, blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,null=True, blank=True)
    paid=models.BooleanField(default=False)
    
    # Add status field with choices
    

    
    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, related_name='customers_wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='wishlist_products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class UserWishlist(models.Model):
    user = models.ForeignKey(CustomUser, related_name='customerswishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='wishlistproducts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



    
    #     total_customers = CustomUser.objects.count()

    #     one_week_ago= timezone.now() - timezone.timedelta(weeks=1)

    #     new_users_last_week = CustomUser.objects.filter(date_joined__gte=one_week_ago).count()

    #     total_orders =OrderItem.objects.count()

        
    #     total_offer_price_amount = Order.objects.aggregate(total_offer_price_amount=Sum('total_price'))


    #     total_amount_received = total_offer_price_amount.get('total_price', 0)
        
    #     total_amount_received //= 1000

    #     order_details_last_week = Order.objects.filter(created_at__gte=one_week_ag
    #     # total_amount_received_last_week = total_amount_received_last_week_details['total_price'] or 0  # Handle None case
    #     # total_amount_received_last_week //= 1000

    #     main_categories = category.objects.annotate(num_product_variants=Count('name'))

    #     category_labels = [category.name for category in main_categories]
    #     category_data = [category.num_product_variants for category in main_categories]

    #     total_products = ProductVariant.objects.count()

    #     time_interval = request.GET.get('time_interval', 'all') # Default to "all" if we're not provided anything
    #     if time_interval == 'yearly':
    #         orders = Order.objects.annotate(date_truncated=TruncYear('created_at', output_field=DateField()))
    #         orders = orders.values('date_truncated').annotate(total_amount=Sum('total_price'))
    #     elif time_interval == 'monthly':
    #         orders = Order.objects.annotate(date_truncated=TruncMonth('created_at',output_field=DateField()))
    #         orders = orders.values('date_truncated').annotate(total_amount=Sum('offer_price'))

    #     monthly_sales = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total_amount=Sum('total_price')).order_by('month')
    #     monthly_labels = [entry['month'].strftime('%B %Y') for entry in monthly_sales]
    #     monthly_data = [float(entry['total_amount'])for entry in monthly_sales]
    #     monthly_data = [float(entry['total_amount']) for entry in monthly_sales]


    #     headers=HttpHeaders(request.headers)
    #     is_ajax_request = headers.get('X-Requested-With')=='XMLHttpRequest'

    #     if is_ajax_request and request.method == 'GET':
    #         time_interval = request.GET.get('time_interval', 'all')
    #         filtered_labels = []
    #         filtered_data = []

    #         if time_interval == 'yearly':
    #             filtered_orders = Order.objects.annotate(
    #                 date_truncated=TruncYear('created_at', output_field=DateField())
    #             )
    #         elif time_interval =='monthly':
    #             filtered_orders = Order.objects.annotate(
    #                 date_truncated=TruncMonth('created_at',output_field=DateField())
    #             )
    #         else:
    #             filtered_orders = Order.objects.annotate(date_truncated=F('created_at'))


    #         filtered_orders = filtered_orders.values('date_truncated')

    #         filtered_orders = filtered_orders.values('date_truncated').annotate(total_amount=Sum('offer_price')).order_by('date_truncated')
    #         filtered_labels = [entry['date_truncated'].strftime('%B %Y') for entry in filtered_orders]
    #         filtered_data = [float(entry['total_amount']) for entry in filtered_orders]
    #         return JsonResponse({"labels": filtered_labels, "data": filtered_data})
        




    #     context={
    #         'top_products':top_products,
    #         'monthly_revenue':monthly_revenue,
    #         'yearly_revenue':yearly_revenue,
    #         "top_products": top_products,
    #         "labels": json.dumps(labels),
    #         "data": json.dumps(data),
    #         "total_customers": total_customers,
    #         "new_users_last_week": new_users_last_week,
    #         "total_orders": total_orders,
            
    #         "total_amount_received": total_amount_received,
            
    #         "total_products": total_products,
    #         "category_labels": json.dumps(category_labels),
    #         "category_data": json.dumps(category_data),
    #         "monthly_labels": json.dumps(monthly_labels),
    #         "monthly_data": json.dumps(monthly_data),
    #     }

    #     if request.method == "GET":
    #     # Get the start and end dates from the request GET parameters
    #         from_date_str = request.GET.get('from_date')
    #         to_date_str = request.GET.get('to_date')

    #         if from_date_str and to_date_str:
    #             from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    #             to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

    #             filtered_orders = Order.objects.filter(created_at__date__range=[from_date, to_date])
    #             filtered_customers = CustomUser.objects.filter(date_joined__date__range=[from_date, to_date])

    #             order_count = 0
    #             if filtered_orders:
    #                 order_count = filtered_orders.count()

    #         # Calculate the total amount received
    #             if filtered_orders.exists():
    #                 total_amount_received = filtered_orders.aggregate(total_price_sum=Sum('total_price'))
    # # Proceed with further processing
    #             else:
    #                 print("No orders match the filtering criteria")
    #         if filtered_orders is not None:
    #             total_amount_received = filtered_orders.aggregate(total_price_sum=Sum('total_price'))
    #             total_amount = total_amount_received.get('total_price_sum', 0)
    #         else:
    #             total_amount = 0  # or any default value you prefer

    #         if isinstance(total_amount_received, dict):
    #             total_amount = total_amount_received.get('total_price_sum', 0)
    #         else:
    #             total_amount = total_amount_received

    #         if total_amount is not None:
    #             total_amount //= 1000  # Assuming you're dealing with currency values
    #         else:
    #             total_amount = 0  # Assuming you're dealing with currency values

    #         # Calculate the total number of customers
    #         if filtered_orders is not None:
    # # Calculate the total amount received
    #             total_amount_received = filtered_orders.aggregate(total_price_sum=Sum('total_price'))
    #             if isinstance(total_amount_received, dict):
    #                 total_amount = total_amount_received.get('total_price_sum', 0)
    #             else:
    #                     total_amount = total_amount_received
    #             if total_amount is not None:
    #                 total_amount //= 1000  # Assuming you're dealing with currency values
    #             else:
    #                 total_amount = 0  # Assuming you're dealing with currency values
    # # Calculate the total number of customers
    #             filtered_customers = set([order.customer for order in filtered_orders])
    #         else:
    #             total_amount = 0
    #             filtered_customers = set()
    #             total_customers = len(filtered_customers)

    # # Assuming you have some logic to calculate total price and labels
    #     if filtered_orders is not None:
    #         data = [float(order.total_price) for order in filtered_orders]
    #         labels = [str(order.id) for order in filtered_orders]

    # # Fetch recent orders
    #     recent_orders = Order.objects.order_by('-id')[:5]


    #         # Update the context with filtered data
    #     context.update({
    #             # 'total_orders': order_count,
    #             'total_amount_received': total_amount,
    #             # 'total_customers': filtered_customers.count(),
    #             "labels": json.dumps(labels),
    #             'data': json.dumps(data),
    #             'recent_orders': recent_orders,
    #         })
        
    #     return render(request, 'admin_auth/index.html', context)
    # return redirect('admin_login')
