from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .forms import  AddressForm,ShippingAddressForm
from .models import Address,ShippingAddress
from accounts.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
# Create your views here.




class AddressCreateView(LoginRequiredMixin, CreateView):
    template_name = 'address/add_form.html'
    form_class = AddressForm
    success_url = 'address:address_list'
 
    def form_valid(self, form):
        request = self.request
        user = User.objects.get(id=request.user.id)
      
        self.object = form.save(commit=False)
        self.object.address_profile = user
        self.object.save()
        messages.success(request, 'The address is sucessfuly enter') 
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        '''
        Return success url
        '''
        return reverse_lazy('address:address_list')







class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'address/update.html'
    form_class = AddressForm
    success_url = 'address:address_list'
    
    def get_queryset(self):
        request = self.request
        user = User.objects.get(id=request.user.pk)
        return Address.objects.filter(address_profile=user)

    def get_success_url(self):
        '''
        Return success url
        '''
        return reverse_lazy('address:address_list')




class ShipppingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'address/add_form.html'
    form_class = ShippingAddressForm
    success_url = 'address:address_list'
 
    def form_valid(self, form):
        request = self.request
        self.object = form.save(commit=False)
      
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        '''
        Return success url
        '''
        return reverse_lazy('cart:checkout')






 
class  AddressListView(LoginRequiredMixin,View):
  template_name = 'address/list.html'
  form_class = ShippingAddressForm
  
  
  def get(self, request, *args, **kwargs):
        form = self.form_class
        request = self.request
        
        try:
            user = User.objects.get(id=request.user.id)
            instance = Address.objects.filter(address_profile=user,address_type="shipping")
           
            context = {
                'form': form,
           
                'instance':instance
                
            }

            

            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an any address")
            return redirect("address:address")

        return render(request, self.template_name,context)
    
  def post(self, request, *args, **kwargs):
        
   
        form = self.form_class(request.POST)
        
        if form.is_valid():
            code = form.cleaned_data['address']
            shipping,data =    ShippingAddress.objects.get_or_create(address=code)
            if shipping:
                shipping.save()
                
        return  HttpResponseRedirect(reverse('cart:checkout'))

        
 
 
       