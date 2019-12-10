from django.urls import path,re_path
from cart import views
app_name = "cart"

urlpatterns = [
    path('<int:product_id>/', views.add_to_cart,name='cart'),
    path('order-summary', views.order_details, name="order_summary"),
    path('delete/<int:product_id>/', views.delete_from_cart, name='delete_item'),
    path('success/', views.success, name='purchase_success'),
    path('checkout/', views.checkout, name='checkout'),
    re_path('update-transaction/(?P<token>[-\w]+)/', views.update_transaction_records,
        name='update_records'),
    path('buy_now/<int:pk>/', views.buy_now,name='buy_now'),

    
    
    
    
]

