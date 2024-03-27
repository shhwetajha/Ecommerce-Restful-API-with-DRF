from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify
from .models import *

# @receiver(pre_save,sender=cart_itemsecond)
# def pre_save(sender,instance,*args,**kwargs):
    
#     cart_id=kwargs['cartsecondid_pk']
#     print('********************************************')

#         # if request.user.is_authenticated:
#             # user=request.user
#             # print(user)
#     print(cart_id)
#         # if instance.slug is None:
#         #     instance.slug=slugify(instance.product_name)