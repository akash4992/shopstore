from django.shortcuts import render,redirect
from coupon.models import Coupons
from coupon.forms import CouponForm
from django.utils import timezone
from django.contrib import messages 
from django.urls import reverse
from django.http import  HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
def get_success_url(self):
    return reverse('products:detail', kwargs={'pk': self.kwargs['pk']})

# def CouponView(request,pk):
#     coupon_id =request.session.get('coupon_id')
   
#     now = timezone.now()
#     form = CouponForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['code']
#         try:
#             coupon = Coupons.objects.get(code__iexact = code,
#                                         valid_from__lte=now,
#                                         valid_to__gte=now,
#                                         active=True )
#             request.session['coupon_id'] = coupon.id
#         except Coupons.DoesNotExist:
#             request.session['coupon_id'] = None
    
#     def get_success_url(request):
#          return reverse_lazy('products:detail', kwargs={'pk':pk})
class CouponView(View):
    form_class = CouponForm()
    def post(self, request, *args, **kwargs):
       coupon_id =request.session.get('coupon_id')
       now = timezone.now()
       form = CouponForm(request.POST)
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
   
    def get_success_url(self):
        return reverse_lazy('product:detail', kwargs={'pk': self.kwargs.get('pk') })