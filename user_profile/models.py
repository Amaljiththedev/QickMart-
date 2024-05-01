from django.utils import timezone
from django.db import models
from user_auth.models import CustomUser
from products.models import ProductVariant, Products


# Create your models here.
class Address(models.Model):
    username = models.ForeignKey(
        CustomUser, related_name="user_name", on_delete=models.CASCADE
    )
    house_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)


class Cart(models.Model):

    user = models.ForeignKey(
        CustomUser, related_name="customername", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True
    )
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=True, blank=True
    )  # Add this line

    product_quantity = models.IntegerField(default=1, null=True, blank=False)
    created_date = models.DateField(default=timezone.now)
    coupon_discount_amount = models.IntegerField(default=0, null=True, blank=False)


class payment(models.Model):
    PAYMENT_CHOICES = [
        ("Cash on delivery", "Cash on delivery"),
        ("walletbalance", "Wallet Balance"),
    ]
    user = models.ForeignKey(
        CustomUser, related_name="customer", on_delete=models.CASCADE
    )
    payment_type = models.CharField(
        max_length=100, choices=PAYMENT_CHOICES, null=True, blank=True
    )


class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Out of delivery", "Out of delivery"),
        ("Return", "Return"),
        ("Refunded", "Refunded"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through="OrderItem")
    address = models.ForeignKey("Address", on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    estimated_delivery_time = models.DateField(null=True, blank=True)
    tracking_number = models.CharField(max_length=10, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    paid = models.BooleanField(default=False)

    # Add status field with choices

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class UserWishlist(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="customerswishlist", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Products, related_name="wishlistproducts", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
