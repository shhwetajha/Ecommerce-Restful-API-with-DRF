from django.dispatch import receiver
from django.db.models.signals import post_save
from fapp.models import Account,UserProfileModel

@receiver(post_save,sender=Account)
def post_save(sender,instance,created,**kwargs):
    if created:
        UserProfileModel.objects.create(user=instance)
