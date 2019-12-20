from django.urls import path,re_path
from coupon import views
app_name = "coupon"

urlpatterns = [
   
    path('code/<int:pk>/', views.CouponView, name="code_summery"),
    
    
    
    
    
]
