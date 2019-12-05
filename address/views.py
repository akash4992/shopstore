from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .forms import  AddressForm
from .models import Address
from accounts.models import User
from django.urls import reverse_lazy
from django.contrib import messages
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



class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'address/list.html'

    def get_queryset(self):
        request = self.request
        user = User.objects.get(id=request.user.id)
        return Address.objects.filter(address_profile=user)



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