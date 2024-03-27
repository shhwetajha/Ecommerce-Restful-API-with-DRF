# Generated by Django 5.0.1 on 2024-03-15 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fapp', '0003_orders'),
        ('products', '0012_variations_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fapp.orders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.products')),
            ],
        ),
    ]
