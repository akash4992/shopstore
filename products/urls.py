from django.urls import path
from products import views
app_name = "products"
urlpatterns = [
    path('home/', views.HomePageView.as_view(),name='home'),
    path('about/',views.AboutPageView.as_view(), name='about'),
    path('data/', views.DataPageView.as_view(), name='data'),  
    
    path(r'', views.ProductListView.as_view(), name='list'),
    path('details/<int:pk>/',views.ProductDetailView.as_view(), name='detail'),
    # path('coupon',views.MyCreateView.as_view(), name='coupon'),
    path('index/',views.index, name='index'),
   
]

