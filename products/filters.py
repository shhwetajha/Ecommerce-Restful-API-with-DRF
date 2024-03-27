from django_filters.rest_framework import FilterSet
from .models import *

class ProductFilter(FilterSet):
    class Meta:
        model=Products
        fields={
            'product_name':['exact'],
            'price':['gt','lt']
        }