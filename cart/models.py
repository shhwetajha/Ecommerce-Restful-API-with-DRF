from django.db import models
from products.models import *
from fapp.models import *
import uuid
from uuid import uuid4


# Create your models here.

class cart(models.Model):
    cart_id=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.cart_id
    
class cart_added(models.Model):
    cart=models.ForeignKey(cart,on_delete=models.CASCADE,null=True,related_name='cartt')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='productt')
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    variations=models.ManyToManyField(variations)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price*self.quantity

    def __unicode__(self):
        return self.product
    
    
class cartsecond(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    user=models.ForeignKey(Account,null=True,blank=True,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.id


    
class cart_itemsecond(models.Model):
    cart=models.ForeignKey(cartsecond,on_delete=models.CASCADE,null=True,related_name='cartsecond')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='productsecond')
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    variations=models.ManyToManyField(variations_added,related_name='variationsadded')
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price*self.quantity

    def __unicode__(self):
        return self.product
    
    def __str__(self):
        return self.product.product_name
    
    
# class cartsecond(models.Model):
#     cart=models.ForeignKey(cartsecond,null=True,on_delete=models.CASCADE)
#     user=models.ForeignKey(Account,null=True,on_delete=models.CASCADE)\
#     product=models.ForeignKey(Products,on_delete=models.CASCADE)