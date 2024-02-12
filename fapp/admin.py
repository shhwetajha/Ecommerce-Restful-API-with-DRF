
from django.contrib import admin
from .models import *

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','username','email','phone',]

admin.site.register(Account,AccountAdmin)
