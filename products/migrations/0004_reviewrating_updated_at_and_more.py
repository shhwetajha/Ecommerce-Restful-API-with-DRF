# Generated by Django 5.0.1 on 2024-02-17 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productgallery_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrating',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
