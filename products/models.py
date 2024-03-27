from django.db import models
from categories.models import *
from fapp.models import *
from django.conf import settings


# Create your models here.


class Products(models.Model):
    product_name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,default=None,null=True)
    description=models.TextField(max_length=100,blank=True)
    images=models.ImageField(upload_to='photos/products')
    stock=models.IntegerField()
    price=models.IntegerField()
    categories=models.ForeignKey(categories,on_delete=models.CASCADE,related_name='products')
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name='product'
        verbose_name_plural='products'


class variationmanager(models.Manager):
    def colors(self,request):
        return super(variationmanager,self).filter(variation_category='color')
    def sizes(self,request):
        return super(variationmanager,self).filter(variation_category='sizes')


variation_category_choice=(
('color','color'),
('sizes','sizes'),
)

class variations(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='variation')
    variation_category=models.CharField(max_length=100,choices=variation_category_choice,default='None')
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    objects=variationmanager()

    class Meta:
        verbose_name='variation'
        verbose_name_plural='variations'


    def __str__(self):
        return self.product.product_name


class productgallery(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE,default='',related_name='gallery')
    images=models.ImageField(upload_to='photos/productgallery')


    def __str__(self):
        return self.product.product_name

class reviewrating(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='reviews')
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=100,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=100,blank=True)
    name=models.CharField(max_length=100,null=True)
    status=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.user.first_name

class productdetail(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    variations=models.OneToOneField(variations,on_delete=models.CASCADE)
    product_gallery=models.ForeignKey(productgallery,on_delete=models.CASCADE)
    craeted_date=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name



class variation_category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class variations_added(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    variation_category=models.ForeignKey(variation_category,on_delete=models.CASCADE)
    variation_value=models.CharField(max_length=100)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.variation_value


