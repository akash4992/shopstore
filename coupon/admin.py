from django.contrib import admin
from coupon.models import Coupons
# Register your models here.



class CouponsAdmin(admin.ModelAdmin):

    list_display = ('code','active','valid_from','valid_to','discount')
    list_filter = ('active','valid_from','valid_to')
    search_fields = ('code',)
    


admin.site.register(Coupons,CouponsAdmin)