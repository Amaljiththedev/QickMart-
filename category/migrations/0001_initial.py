# Generated by Django 5.0.2 on 2024-03-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=255, unique=True)),
                ('logo', models.ImageField(blank=True, upload_to='brand_logo')),
            ],
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='category_media')),
                ('description', models.TextField()),
                ('category_offer_description', models.TextField(blank=True, null=True)),
                ('category_offer', models.PositiveBigIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
