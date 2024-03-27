from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify
from .models import Products

@receiver(pre_save,sender=Products)
def pre_save(sender,instance,*args,**kwargs):
    if instance.slug is None:
        instance.slug=slugify(instance.product_name)