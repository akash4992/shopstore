from cart.models import Order
from django import template

register = template.Library()

@register.simple_tag
def cart_item_count(user):
    try:
        count = Order.objects.filter(owner__username = user, is_ordered=False)[0].items.count()
        return count
    except:
        return 0

    
