from accounts.models import User
from products.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from cart.extra import generate_order_id
from .models import Transaction,ProductCart,OrderProduct
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cart.extra import generate_order_id
from django.conf import settings
import datetime
import stripe
from django.db import IntegrityError
from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your vews here.

def get_user_pending_order(request,key):
    order = OrderProduct.objects.filter(session_key=key,is_ordered=False)
    if order.exists():
        return order[0]
    return 0
    if  request.user.is_authenticated:
        user_profile = get_object_or_404(User,pk= request.user.pk)
        order = OrderProduct.objects.filter(owner=user_profile,session_key=key,is_ordered=False)
        if order.exists():
            return order[0]
        return 0
        
   

# @login_required(login_url='/accounts/login/')
# def buy_now(request,**kwargs):
    
#     user_profile = get_object_or_404(User,pk= request.user.pk)
 
#     product = Product.objects.filter(id=kwargs.get('pk', "")).first()
    
#     order_item, status = OrderItem.objects.get_or_create(product=product)

#     user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
#     user_order.items.add(order_item)
#     if status:
#         user_order.ref_code = generate_order_id()
#         user_order.save()
        
#     return redirect(reverse('address:address_list'))



@login_required(login_url='/accounts/login/')
def buy_now(request,**kwargs):
    if request.method == 'POST':
        product_id=request.POST['product_id']
        product =  Product.objects.filter(id=product_id).first()
        product_title = request.POST['product_title']
        product_price = request.POST['product_price']
     
        data  = ProductCart(product =product,
                            amount=product_price,
                            productname= product_title,
                            is_ordered=  False, )
        data.ref_code = generate_order_id()
        try:
            data.save()
        except:
            pass
        cart = settings.CART_SESSION_ID
        the_id = request.session['cart_id'] = cart
    if  request.user.is_authenticated:
        user_profile = get_object_or_404(User,pk= request.user.pk)
        if user_profile:
            user_profile = get_object_or_404(User,pk= request.user.pk)
            order_item ,created = ProductCart.objects.get_or_create(product=product_id)
            user_order,created = OrderProduct.objects.get_or_create(owner=user_profile ,is_ordered=False,defaults = {'session_key': the_id})
            

            user_order.items.add(order_item)
            user_order.ref_code = generate_order_id()
            user_order.save()
        
    return redirect(reverse('address:address_list'))









def order_details(request, **kwargs):
    key = request.session.get('cart_id')
   
    existing_order = get_user_pending_order(request,key)
    print("the order",existing_order)
    context = {
        'order': existing_order
    }
    return render(request, 'cart/home.html', context)

def delete_from_cart(request,product_id):

    item_to_delete = ProductCart.objects.filter(pk=product_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()

    return redirect(reverse('cart:order_summary'))





@login_required(login_url='/accounts/login/')
def checkout(request, **kwargs):
    key = request.session.get('cart_id')
    if key:
        existing_order = get_user_pending_order(request,key)
    else:
        cart = settings.CART_SESSION_ID
        key = request.session['cart_id'] = cart
        existing_order = get_user_pending_order(request,key)

    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100*existing_order.get_cart_total(),
                    currency='inr',
                    description='Prodcut charge',
                    source=token,
                )

                return redirect(reverse('cart:update_records',
                        kwargs={
                            'token': token
                        })
                    )
            except stripe.error.CardError:
                messages.info(request, "Your card has been declined.")
        else:
            result = transact({
                'amount': existing_order.get_cart_total(),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                return redirect(reverse('cart:update_records',
                        kwargs={
                            'token': result.transaction.id
                        })
                    )
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('cart:checkout'))
            
    context = {
        'order': existing_order,
    
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'cart/checkout.html', context)

@login_required()
def update_transaction_records(request, token):
    key = request.session.get('cart_id')
  
    order_purchase = get_user_pending_order(request,key)
    order_purchase.is_ordered=True
    order_purchase.date_ordered=datetime.datetime.now()
    order_purchase.save()
    
    order_items = order_purchase.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
    user_profile = get_object_or_404(User, username=request.user.username)
    amount = order_purchase.get_cart_total()
    transaction = Transaction(username = user_profile,
                            token=token,
                            order_id= order_purchase.id,
                            amount=  amount,
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()


    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('accounts:my_profile'))


def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'cart/purchase_success.html', {})






# def add_to_cart(request,**kwargs):
#     request.session.set_expiry(864000)
    
    
#     if request.POST.get('action') == 'post':
#         size = request.POST.get('size')
#         import pdb; pdb.set_trace()
#         product_id=request.POST['product_id']
#         product =  Product.objects.filter(id=product_id).first()
#         product_title = request.POST['product_title']
#         product_price = request.POST['product_price']
     
#         data  = ProductCart(product =product,
#                             amount=product_price,
#                             productname= product_title,
#                             is_ordered=  False, )
#         data.ref_code = generate_order_id()
#         try:
#             data.save()
#         except:
#             pass
    
        
#         cart = settings.CART_SESSION_ID
#         the_id = request.session['cart_id'] = cart
#     if not request.user.is_authenticated:
#         order_item ,created = ProductCart.objects.get_or_create(product=product_id)
#         user_order,created = OrderProduct.objects.get_or_create(defaults = {'owner': None},is_ordered=False,session_key=the_id)
#         user_order.items.add(order_item)
#         user_order.ref_code = generate_order_id()
#         user_order.save()
        
#     else:
#         user_profile = get_object_or_404(User,pk= request.user.pk)
#         if user_profile:
#             user_profile = get_object_or_404(User,pk= request.user.pk)
#             order_item ,created = ProductCart.objects.get_or_create(product=product_id)
#             user_order,created = OrderProduct.objects.get_or_create(owner=user_profile ,is_ordered=False,defaults = {'session_key': the_id})
            

#             user_order.items.add(order_item)
#             user_order.ref_code = generate_order_id()
#             user_order.save()
        
#     messages.success(request, "item added to cart")
        
#     return redirect(reverse('products:list'))


def add_to_cart(request,**kwargs):
    request.session.set_expiry(864000)
    

    if request.POST.get('action') == 'post':
        psize = request.POST.get('size')
        
        product_id= request.POST.get('product_id')
        product =  Product.objects.filter(id=product_id).first()
        product_title = request.POST.get('product_title')
        product_price = request.POST.get('product_price')
     
        
        

        update,data  = ProductCart.objects.get_or_create(product =product,
                            amount=product_price,
                            productname= product_title,
                            is_ordered=  False,
                            size= psize ,
                             )
        update.ref_code = generate_order_id()
        if data:
            update.Quantity = update.Quantity+1
            update.save()
        else:
            update.save()
        
    
        
        cart = settings.CART_SESSION_ID
        the_id = request.session['cart_id'] = cart
    if not request.user.is_authenticated:
        order_item ,created = ProductCart.objects.get_or_create(product=product_id)
        user_order,created = OrderProduct.objects.get_or_create(defaults = {'owner': None},is_ordered=False,session_key=the_id)
        user_order.items.add(order_item)
        user_order.ref_code = generate_order_id()
        user_order.save()
        
    else:
        user_profile = get_object_or_404(User,pk= request.user.pk)
        if user_profile:
            user_profile = get_object_or_404(User,pk= request.user.pk)
            order_item ,created = ProductCart.objects.get_or_create(product=product_id)
            user_order,created = OrderProduct.objects.get_or_create(owner=user_profile ,is_ordered=False,defaults = {'session_key': the_id})
            

            user_order.items.add(order_item)
            user_order.ref_code = generate_order_id()
            user_order.save()
    messages.success(request, "item added to cart")     
    return JsonResponse({'message': "item added to cart"})   
        
    

	
    
  

 




