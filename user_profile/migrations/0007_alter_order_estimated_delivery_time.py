# Generated by Django 5.0.2 on 2024-03-26 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_profile", "0006_order_estimated_delivery_time_order_tracking_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="estimated_delivery_time",
            field=models.DateField(blank=True, null=True),
        ),
    ]
