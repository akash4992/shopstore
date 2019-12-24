from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as autherize, login as customlogin,logout

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

from django.template import RequestContext
from cart.models import OrderProduct
from .models import User


def my_profile(request):
  
    key = request.session.get('cart_id')
    my_user_profile =  User.objects.filter(username=request.user.username).first()
    my_orders = OrderProduct.objects.filter(session_key=key,is_ordered=True,owner=my_user_profile) 
    context ={
        "my_orders":my_orders
    }
    
    return render(request, "accounts/profile.html",context)


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


 
  


# def login_request(request):
#     if request.user.is_authenticated:
#         return redirect('address:address_list')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('products:list'))
            
#         else:
#             messages.warning(request, 'Your have enter wrong email and password') 
#             return render(request, 'accounts/login.html', {})
#     else:
#         return render(request, 'accounts/login.html', {})



def login_request(request):

    state = "Please log in below..."
    username = password = ''

    next = ""

    if request.GET:  
        next = request.GET['next']

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = autherize(username=username, password=password)
        if user is not None:
            if user.is_active:
                customlogin(request, user)
                
                state = "You're successfully logged in!"
                if next == "":
                    

                      
                    return HttpResponseRedirect(reverse('products:list'))
                else:
                    user_profile = User.objects.get(id=request.user.id)
                   
                    if user_profile:
                        update ,data = OrderProduct.objects.get_or_create(owner=None)
                        
                        if update:
                            update.owner = user_profile
                            update.save()
   
                    return redirect('address:address_list')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    context= {
        'state':state,
        'username': username,
        'next':next,
    }
    return render(request,'accounts/login.html',context)
    
        
    



from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "accounts/home.html"