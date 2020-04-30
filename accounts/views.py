from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import  NewUserForm,LoginForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.shortcuts import render, get_object_or_404

from cart.models import Order
from .models import User


def my_profile(request):
	my_user_profile = User.objects.filter(username=request.user.username).first()
	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
	context = {
		'my_orders': my_orders
	}

	return render(request, "accounts/profile.html", context)
# Create your views here.

class Register(generic.CreateView):
    template_name = 'accounts/signup.html'
    form_class = NewUserForm
    success_url = 'accounts:login'

    

    def get_success_url(self):
        '''
        Return success url
        '''
        return reverse_lazy('accounts:login')


 
  


def login_request(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('products:list'))
            
        else:
            messages.warning(request, 'Your have enter wrong email and password') 
            return render(request, 'accounts/login.html', {})
    else:
        return render(request, 'accounts/login.html', {})







