
from django.conf import settings

def cart(request):
    cart = settings.CART_SESSION_ID
    return {'cart':cart}

