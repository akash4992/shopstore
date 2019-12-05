from django.urls import path
from category import views
app_name = "category"

urlpatterns = [

    path('list/', views.CategoryListView.as_view(), name='category_list'),
    path('category_type/<int:pk>/', views.CategorytypeListView.as_view(), name='category_type'),
    path('category_product/<int:pk>/', views.ProductListCategory.as_view(), name='category_product'),
    
  
    
]

