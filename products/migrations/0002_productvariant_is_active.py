# Generated by Django 5.0.2 on 2024-03-23 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
