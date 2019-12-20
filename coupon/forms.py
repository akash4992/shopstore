from django import forms
from coupon.models import Coupons


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = ('code',)
 