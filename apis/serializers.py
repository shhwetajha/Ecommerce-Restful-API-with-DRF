from rest_framework import serializers
from products.models import *
from categories .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=['product_name','description','images','stock']


class categoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=categories
        fields=['category_name','description','images']