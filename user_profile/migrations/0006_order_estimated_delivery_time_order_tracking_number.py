# Generated by Django 5.0.2 on 2024-03-26 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='estimated_delivery_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]