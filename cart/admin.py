from django.contrib import admin
from .models import Transaction,ProductCart,OrderProduct
from address.models import Address



class OrderProductAdmin(admin.ModelAdmin):
    
    model = OrderProduct

    readonly_fields = ('address_profile','address_line_1','address_line_2','date_ordered', 'name', 'city','address_type','country', 'state', 'postal_code', 'mobile_no' )
    
    
    fieldsets = (
        ('Order Products', {
            'fields': ('ref_code', 'is_ordered', 'items', 'date_ordered','session_key', 'code', 'discount')
        }),
        ('Shipping Address', {
            'fields': ('address_profile','name', 'address_line_1','address_line_2', 'city','address_type','country', 'state', 'postal_code', 'mobile_no' )
        }),
    )

    def address_line_1(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).address_line_1
    
    def name(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).name
    
    def city(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).city
    
    def address_type(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).address_type
    
    def address_profile(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).address_profile
    
        
    def address_line_2(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).address_line_2

    def country(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).country
    
    def state(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).state

    def postal_code(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).postal_code

    def mobile_no(self, obj):
        user_id = obj.owner_id
        return Address.objects.get(address_profile=user_id ).mobile_no

admin.site.register(Transaction)
admin.site.register(ProductCart)
admin.site.register(OrderProduct,OrderProductAdmin)

