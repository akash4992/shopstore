from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    """
    User-related CRUD form
    """
    class Meta:
        model = Address
        fields = [
            'nickname',
            'name',
            'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code',
            'mobile_no'  
        ]