# Generated by Django 5.0.4 on 2024-04-09 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productvariant_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariant',
            old_name='size',
            new_name='inch',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='internal_storage',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='ram',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]