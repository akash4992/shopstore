from django.contrib import admin

# Register your models here.
from .models import Product




class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','description', 'price', 'image','featured','active','is_digital']

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)