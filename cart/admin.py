from django.contrib import admin

from .models import Transaction,ProductCart,OrderProduct


admin.site.register(Transaction)
admin.site.register(ProductCart)
admin.site.register(OrderProduct)
