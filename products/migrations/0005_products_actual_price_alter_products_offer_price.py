# Generated by Django 5.0.4 on 2024-04-23 09:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_products_offer_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="actual_price",
            field=models.DecimalField(decimal_places=2, default="0", max_digits=10),
        ),
        migrations.AlterField(
            model_name="products",
            name="offer_price",
            field=models.DecimalField(
                decimal_places=2,
                default=1,
                max_digits=5,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
            preserve_default=False,
        ),
    ]
