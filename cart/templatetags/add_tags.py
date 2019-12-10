from cart.models import OrderProduct
from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag
def cart_item_count(user,key):
    try:
        count = OrderProduct.objects.filter(owner__username =user,session_key=key,is_ordered=False)[0].items.count()
        return count
    except:
        return 0



