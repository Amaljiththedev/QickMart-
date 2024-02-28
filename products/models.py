from category.models import category as Category 
from category.models import Brand as Brand
from django.db import models

# Create your models here.
class Products(models.Model):
    Status_choices=(
        ('In Stock', 'In Stock'),
        ('Out Stock', 'Out Stock'),
    )
    
    title=models.CharField(max_length=255,null=False)
    # representing the title of the product.
    category = models.ForeignKey(Category, related_name='category_name', on_delete=models.CASCADE)
    # ForeignKey to the Category model, establishing a many-to-one relationship between products and categories.
    description=models.TextField()
    # TextField for the product description.
    price=models.PositiveIntegerField(null=True)
    # price: PositiveIntegerField representing the price of the product.
    brand=models.ForeignKey(Brand,related_name='Brand_name',on_delete=models.CASCADE)
    # brand: CharField with choices representing various brands.
    status=models.CharField(max_length=100,choices=Status_choices)
    # status: CharField with choices representing the status of the product (In Stock/Out Stock).
    stock_count=models.IntegerField(default=0)
    # stock_count: IntegerField representing the count of items in stock.
    image = models.ImageField(upload_to='products/')
    # image: ImageField for uploading product images.
    sku = models.CharField(max_length=50)
    # sku: CharField representing the Stock Keeping Unit of the product.
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # weight: DecimalField representing the weight of the product.
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    # dimensions: CharField representing the dimensions of the product.
    available = models.BooleanField(default=True)
    # available: BooleanField indicating whether the product is available.
    featured = models.BooleanField(default=False)
    # featured: BooleanField indicating whether the product is featured.
    created_date = models.DateTimeField(auto_now_add=True)
    # created_date: DateTimeField set to auto_now_add, automatically set to the creation date of the object.
    updated_date = models.DateTimeField(auto_now=True)
    # updated_date: DateTimeField set to auto_now, automatically set to the last update date of the object.
    is_active=models.BooleanField(default=True)
    # is_active: BooleanField set to True
    def __str__(self):
        return self.title

    
class Product_images(models.Model):
    product = models.ForeignKey(Products, related_name='images', on_delete=models.CASCADE)
    product_image1 = models.ImageField(upload_to='products/images/')
    product_image2 = models.ImageField(upload_to='products/images/')
    product_image3 = models.ImageField(upload_to='products/images/')
    product_image4 = models.ImageField(upload_to='products/images/')
    product_image5 = models.ImageField(upload_to='products/images/')

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
    
    
    
