from django.contrib import admin
from .models import Address, ShippingAddress

# Register your models here.

class AdressAdmin(admin.ModelAdmin):
    class Meta:
        model = Address
        fields = ['id','address_profile', 'name',  'nickname','address_type','address_line_1','address_line_2','city']


admin.site.register(Address,AdressAdmin)
admin.site.register(ShippingAddress)