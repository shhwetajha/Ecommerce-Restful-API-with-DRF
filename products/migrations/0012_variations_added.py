# Generated by Django 5.0.1 on 2024-03-01 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_variation_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='variations_added',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_value', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('variation_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variation_category')),
            ],
        ),
    ]
