from django.urls import path
from django.conf import urls
from accounts import views
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy
app_name = "accounts"

urlpatterns = [
    path('register/',views.Register.as_view(),name='register'),
    path('login/', views.login_request, name="login"),
    path('logout/', auth_views.LogoutView.as_view(
        next_page=reverse_lazy('accounts:login'),
    ), name='logout'),
    path('profile/', views.my_profile, name='my_profile')
    
    
  
    
]

