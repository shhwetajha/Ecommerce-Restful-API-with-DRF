# Generated by Django 5.0.1 on 2024-02-28 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_products_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(default=None, max_length=100, null=True, unique=True),
        ),
    ]
