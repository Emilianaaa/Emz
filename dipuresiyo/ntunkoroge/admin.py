from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']#identifiable keyword to type in url

    list_display = ['name', 'price', 'created_by','in_stock','is_available']
    list_filter = ['is_available']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']#identifiable keyword to type in url

    list_display = ['name','slug', 'description']
    list_filter = ['name']
    list_editable = ['description']
    prepopulated_fields = {'slug':('name',)}
