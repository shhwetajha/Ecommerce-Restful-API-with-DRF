from rest_framework import serializers
from .models import *
from products.models  import *
from products.serializers import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Products
        fields=['product_name','description','images','stock']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=categories

