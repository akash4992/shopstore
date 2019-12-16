from django.contrib import admin

# Register your models here.
from .models import Product,Productsize



class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','description', 'price', 'image','active','is_digital']

    class Meta:
        model = Product

class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product','value', 'stock', 'items_sold']

    class Meta:
        model = Productsize



admin.site.register(Product,ProductAdmin)
admin.site.register(Productsize,ProductSizeAdmin)
