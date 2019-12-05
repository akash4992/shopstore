from django.contrib import admin
from .models import View
# Register your models here.


class ViewAdmin(admin.ModelAdmin):
    
    fields = ['user','product','view_counts']
    list_display = ['product','view_counts','product_user']

    def product_user(self, obj):
        return "\n".join([u.username for u in obj.user.all()])
    class Meta:
        model = View

    


admin.site.register(View,ViewAdmin)