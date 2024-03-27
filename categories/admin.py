from django.contrib import admin
from .models import *

# Register your models here.

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=['id','category_name','slug']

admin.site.register(categories,categoryAdmin)



