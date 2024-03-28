from django.db import models
from rest_framework.views import APIView
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from product.views import *

# Create your models here.

class categories(models.Model):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,default=None,null=True,unique=True)
    description=models.CharField(max_length=100,blank=True)
    images=models.ImageField(upload_to='photos/categories',null=True)


    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

    # def save(self,*args,**kwargs):
    #     if self.slug is None:
    #         self.slug=slugify(self.category_name)
    #         super().save(*args,**kwargs)

    # class get_url(APIView):
    #     def get(self,request):
    #         return reverse(categorydetail,args={'self.category_slug'})
   
    def __str__(self):
        return self.category_name


# class Student(models.Model):
#     name=models.CharField(max_length=100)
#     age=models.IntegerField()
#     roll_no=models.IntegerField()

