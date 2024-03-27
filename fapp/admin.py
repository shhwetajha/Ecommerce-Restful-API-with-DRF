
from django.contrib import admin
from .models import *

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','username','email','phone',]


class OrdersAdmin(admin.ModelAdmin):
    list_display=['id','placed_at','payment_status','owner','order_payment_id']

class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id','order','product','quantity',]

class UserProfileAdmin(admin.ModelAdmin):
    list_display=['id','address_line_1','address_line_2','profile_picture','user','state','city','country']


admin.site.register(Account,AccountAdmin)
admin.site.register(Orders,OrdersAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(UserProfileModel,UserProfileAdmin)
