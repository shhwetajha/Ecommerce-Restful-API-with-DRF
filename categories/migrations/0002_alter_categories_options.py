# Generated by Django 5.0.1 on 2024-02-15 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
    ]
