from django.contrib import admin

from .models import Transaction,ProductCart,OrderProduct, Order,OrderItem


admin.site.register(Transaction)
admin.site.register(ProductCart)
admin.site.register(OrderProduct)
admin.site.register(OrderItem)
admin.site.register(Order)