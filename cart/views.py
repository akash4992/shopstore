from accounts.models import User
from products.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from cart.extra import generate_order_id
from .models import OrderItem,Order,Transaction
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cart.extra import generate_order_id, transact, generate_client_token
from django.conf import settings
import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your vews here.




def get_user_pending_order(request):
    user_profile = get_object_or_404(User,pk= request.user.pk)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0

@login_required(login_url='/accounts/login/')
def add_to_cart(request,**kwargs):
    
    user_profile = get_object_or_404(User,pk= request.user.pk)
 
    product = Product.objects.filter(id=kwargs.get('pk', "")).first()
    
    order_item, status = OrderItem.objects.get_or_create(product=product)

    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
       
        user_order.ref_code = generate_order_id()
        user_order.save()

    
    messages.success(request, "item added to cart")
    
    return redirect(reverse('products:list'))
 
@login_required(login_url='/accounts/login/')
def buy_now(request,**kwargs):
    
    user_profile = get_object_or_404(User,pk= request.user.pk)
 
    product = Product.objects.filter(id=kwargs.get('pk', "")).first()
    
    order_item, status = OrderItem.objects.get_or_create(product=product)

    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
       
        user_order.ref_code = generate_order_id()
        user_order.save()
        
    return redirect(reverse('address:address_list'))



@login_required(login_url='/accounts/login/')
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'cart/home.html', context)

@login_required(login_url='/accounts/login/')
def delete_from_cart(request, pk):
    item_to_delete = OrderItem.objects.filter(pk=pk)
    if item_to_delete.exists():
        item_to_delete[0].delete()
    return redirect(reverse('cart:order_summary'))





@login_required(login_url='/accounts/login/')
def checkout(request, **kwargs):

    existing_order = get_user_pending_order(request)
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
    order_purchase = get_user_pending_order(request)
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
