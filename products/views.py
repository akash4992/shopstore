
from django.views.generic import TemplateView
from django.contrib import messages

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from analytics.models import View
from .models import Product,Productsize
# Create your views here.

class HomePageView(TemplateView):
    template_name = "base/index.html"


class AboutPageView(TemplateView):
    template_name = "base/about.html"

class DataPageView(TemplateView):
    def get(self, request, **kwargs):
        data =  Product.objects.all()
        context = {
            'data': data
        }
        
        return render(request, 'base/data.html', context)





class ProductListView(ListView):
    '''List of the products'''
   
    template_name = "products/list.html"

  

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        
        return Product.objects.all()


class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get(id=pk)
        
        if instance:
            view,created  = View.objects.get_or_create(
                product=instance
            )
            if view:
                if not request.user.is_authenticated:
               
                    view.view_counts +=1
                            
                    view.save()
                    return instance
                else:
                    view.user.add(request.user)
                    view.view_counts +=1
                    view.save()
                    return instance
        else:
            raise Http404("Product doesn't exist")
        
from django.http import HttpResponse
from products.tasks import sleepy,send_email_task
def index(request):
    send_email_task()
    return HttpResponse("<h1>EMAIL HAS BEEN SEND</H1>")






  