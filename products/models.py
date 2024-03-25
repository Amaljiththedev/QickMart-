from category.models import category as Category 
from category.models import Brand as Brand
from django.db import models


class Products(models.Model):
    Status_choices = (
        ('In Stock', 'In Stock'),
        ('Out Stock', 'Out Stock'),
    )

    title = models.CharField(max_length=255, null=False, unique=True)
    category = models.ForeignKey(Category, related_name='category_name', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.PositiveIntegerField(null=True)
    brand = models.ForeignKey(Brand, related_name='Brand_name', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=Status_choices)
    stock_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    trending = models.BooleanField(default=False)
    product_details=models.TextField(null=True, blank=True)
    variants = models.ManyToManyField('ProductVariant', related_name='products', blank=True)

    def __str__(self):
        return self.title

class ProductVariant(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_variants')
    price = models.PositiveIntegerField(null=True)
    stock_count = models.IntegerField(default=0)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.title} - {self.size} - {self.color}"

class VariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='variant_images', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.variant.product.title} - {self.variant.size} - {self.variant.color}"

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='product_images', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.title}"

class product_review(models.Model):
    stars= [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
]
    Title=models.ForeignKey(Products,related_name='reviews',on_delete=models.CASCADE)
    review=models.CharField(max_length=1, choices=stars)
    
    def _str_(self):
        return self.review