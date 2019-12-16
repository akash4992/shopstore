import django_filters
from .models import ProductSize
from django import forms
class ProductFilter(django_filters.FilterSet):
    product_size=django_filters.ModelMultipleChoiceFilter(
        queryset= ProductSize.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
  

    class Meta:
        model = ProductSize
        fields=['product_size']