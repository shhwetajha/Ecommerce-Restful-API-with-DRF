from django.contrib import admin
from .models import *
import admin_thumbnails


# Register your models here.


@admin_thumbnails.thumbnail('images')
class ProductgalleryInline(admin.TabularInline):
    model= productgallery
    extra=1
    

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=['id','product_name','slug','description','price','stock','is_available']
    inlines=[ProductgalleryInline]

class variationadmin(admin.ModelAdmin):
    list_display=['product','variation_category','variation_value','is_active']
    list_editable=['is_active']
    list_filter=['product','variation_category','variation_value','is_active']

class reviewratingadmin(admin.ModelAdmin):
    list_display=['product','user','subject','review','rating']

class productdetailadmin(admin.ModelAdmin):
    list_display=['product','variations','product_gallery']

class variations_addedadmin(admin.ModelAdmin):
    list_display=['id','product','variation_category','variation_value']






admin.site.register(Products,ProductAdmin)
admin.site.register(variations,variationadmin)
admin.site.register(reviewrating,reviewratingadmin)
admin.site.register(productdetail,productdetailadmin)
admin.site.register(variation_category)
admin.site.register(variations_added,variations_addedadmin)

