from django.contrib import admin
from .models import *

# Register your models here.
class cartadmin(admin.ModelAdmin):
    list_display=['cart_id']

class cartitemadmin(admin.ModelAdmin):
    list_display=['cart','product','user','quantity']

class cartitemsecondadmin(admin.ModelAdmin):
    list_display=['id','cart','product','quantity']

admin.site.register(cart,cartadmin)
admin.site.register(cart_added,cartitemadmin)
admin.site.register(cartsecond)
admin.site.register(cart_itemsecond,cartitemsecondadmin)

