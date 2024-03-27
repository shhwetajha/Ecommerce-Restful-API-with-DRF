from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import categories

@receiver(pre_save,sender=categories)
def pre_save(sender,instance,*args,**kwargs):
    if instance.slug is None:
        instance.slug=slugify(instance.category_name)
