from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True, unique=True)
    image = models.ImageField(upload_to="category_media", blank=True)
    description = models.TextField(null=False, blank=False)
    category_offer_description = models.TextField(blank=True, null=True)
    category_offer = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    brand_name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="brand_logo", blank=True)

    def __str__(self):
        return self.brand_name
