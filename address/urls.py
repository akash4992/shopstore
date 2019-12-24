from django.urls import path
from address import views



app_name = "address"

urlpatterns = [
    path('address/',views.AddressCreateView.as_view(),name='address'),
    path('addresslist', views.AddressListView.as_view(), name='address_list'),
    path('address/<int:pk>/', views.AddressUpdateView.as_view(), name='address-update'),
    path('shipping', views.ShipppingCreateView.as_view(), name='shipping_address'),
   
    
]

