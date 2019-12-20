from decimal import Decimal
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from datetime import datetime
from coupon.models import Coupons
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
User = settings.AUTH_USER_MODEL



class Transaction(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']



class ProductCart(models.Model):
     
 
    product = models.OneToOneField(Product,on_delete=models.CASCADE,blank=True,null=True,unique=False)
    amount = models.DecimalField(max_digits=100,decimal_places=2)
    productname=models.CharField(max_length=200)
    is_ordered = models.BooleanField(default= False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    Quantity=models.IntegerField(default=1)
    ref_code = models.CharField(max_length= 15)
    session_key = models.CharField(max_length=40,blank=True,null=True)
    size =  models.CharField(max_length= 15,blank=True,null=True)
    
    def __str__(self):
        return '{0} - {1}'.format(self.productname, self.ref_code)
    
    
    

class OrderProduct(models.Model):
    owner = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length= 15)
    is_ordered = models.BooleanField(default= False)
    items = models.ManyToManyField(ProductCart)
    date_ordered = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40,blank=True,null=True)
    code = models.ForeignKey(Coupons,null=True,blank=True,on_delete=models.CASCADE)
    discount = models.IntegerField(null=True,blank=True,validators=[MinValueValidator(0),MaxValueValidator(100)])

    def get_cart_items(self):

        return self.items.all()

    def get_cart_total(self):
        total_price =  sum([item.product.price * item.Quantity for item in self.items.all()])
        return total_price - total_price * self.discount/Decimal('100')

    def __str__(self):
        return '{0}'.format(self.ref_code)




