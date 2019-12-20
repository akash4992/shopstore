
from django.views.generic import TemplateView
from django.contrib import messages

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from analytics.models import View
from .models import Product,Productsize
from coupon.models import Coupons
from coupon.views import CouponView
from coupon.forms import CouponForm
from django.views import View
from coupon.models import Coupons
from django.http import  HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.urls import reverse
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse

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
    paginate_by = 6
  

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        
        return Product.objects.all()


# class ProductDetailView(DetailView):
#     #queryset = Product.objects.all()
#     template_name = "products/detail.html"

#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        
#         return context

#     def get_object(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         instance = Product.objects.get(id=pk)
        
#         if instance:
#             view,created  = View.objects.get_or_create(
#                 product=instance
#             )
#             if view:
#                 if not request.user.is_authenticated:
               
#                     view.view_counts +=1
                            
#                     view.save()
#                     return instance
#                 else:
#                     view.user.add(request.user)
#                     view.view_counts +=1
#                     view.save()
#                     return instance
#         else:
#             raise Http404("Product doesn't exist")
            
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         coupon =   Coupons.objects.all()
#         form = CouponForm()
    
#         context['coupon'] =  coupon
#         context['form'] =  form
#         return context


class ProductDetailView(View):
  template_name = 'products/detail.html'
  form_class = CouponForm
  
  
  def get(self, request, *args, **kwargs):
        form = self.form_class
        request = self.request
        pk = self.kwargs.get('pk')
        try:
            coupon = Coupons.objects.filter(active=True)
            instance = Product.objects.get(id=pk)
           
            context = {
                'form': form,
                'coupon': coupon,
                'instance':instance
                
            }

            

            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("products:list")

        return render(request, self.template_name,context)

  def post(self, request, *args, **kwargs):
    coupon_id =request.session.get('coupon_id')
    now = timezone.now()
    form = self.form_class(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupons.objects.get(code__iexact = code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True )

            request.session['coupon_id'] = coupon.id
            
        except Coupons.DoesNotExist:
            request.session['coupon_id'] = None
        messages.info(self.request, "Coupon is applied")
        return  HttpResponseRedirect(reverse('products:detail',  kwargs={'pk': self.kwargs.get('pk') } ))
    else:
      return render(request, self.template_name, {'form': form})
   

    
        
from django.http import HttpResponse
from products.tasks import sleepy,send_email_task
# def index(request):
#     send_email_task()
#     return HttpResponse("<h1>EMAIL HAS BEEN SEND</H1>")



def index(request):
    return render (request,'products/couponform.html')
