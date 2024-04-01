from rest_framework import serializers
from .models import *
from products.models  import *
from products.serializers import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Products
        fields=['id','product_name','description','images','stock']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=categories


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Student
#         fields='__all__'


#     def create(self,validated_data):
#         return Student.objects.create(**validated_data)

