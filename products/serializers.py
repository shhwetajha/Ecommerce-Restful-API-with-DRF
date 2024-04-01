from rest_framework import serializers
from products.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= categories
        fields=['category_name','description','images']


class variationSerializer(serializers.ModelSerializer):
    class Meta:
        model=variations
        fields=['variation_category','variation_value']

class ProductgallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = productgallery
        fields=['images']


class reviewratingserialzer(serializers.ModelSerializer):
    class Meta:
        model=reviewrating
        fields=['subject','review','rating']

    def validate(self,attrs):
        subject=attrs.get('subject')
        review=attrs.get('review')
        rating=attrs.get('rating')
        user=self.context.get('user')
        product=self.context.get('product')
        data=reviewrating()
        data.user=user
        data.product=product
        data.subject=subject
        data.review=review
        data.rating=rating
        data.save()
        return attrs


class Reviewupdateserializer(serializers.ModelSerializer):
    class Meta:
        model=reviewrating
        fields=['subject','review','rating']


class ProductSerializer(serializers.ModelSerializer):
    variation=variationSerializer(many=True,read_only=True)
    gallery=ProductgallerySerializer(many=True, read_only=True)
    reviews=Reviewupdateserializer(many=True,read_only=True)
    class Meta:
        model=Products
        fields=['product_name','description','images','stock','price','variation','gallery','reviews','categories',]

    categories=CategorySerializer()

class ProductSerial(serializers.ModelSerializer):
    gallery=ProductgallerySerializer(many=True,read_only=True)
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length = 1000000,allow_empty_file = True,use_url = False),write_only=True)

    class Meta:
        model=Products
        fields=['id','product_name','description','images','stock','price','categories','gallery','uploaded_images']

    def create(self,validated_data):
        imagess=validated_data.pop('uploaded_images')
        productt=Products.objects.create(**validated_data)
        for i in imagess:
            productgallery.objects.create(product=productt,images=i)
        return productt




class ReviewRatinggSerializer(serializers.ModelSerializer):
    class Meta:
        model=reviewrating
        fields=['subject','review','rating','name']

    def create(self,validated_data):
        product_id=self.context['product_id']
        user=self.context['user']
        return reviewrating.objects.create(product_id=product_id,user=user,**validated_data)

class variation_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=variation_category
        fields=['name']
class variations_addedSerializer(serializers.ModelSerializer):
    variation_category=variation_categorySerializer(many=False,read_only=True)
    class Meta:
        model=variations_added
        fields=['id','variation_category','variation_value']
