import django_filters
from products.models import Product
from django import forms
class ProductFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending','Ascending'),
        ('descending','Descending'),
    )
    ordering = django_filters.ChoiceFilter(label='Ordering',choices=CHOICES,method='filter_by_ordering')
    
  

    class Meta:
        model = Product
        fields={
            'title' :['icontains']
        }

    def filter_by_ordering(self,queryset,name,value):
        expression = 'created' if value == 'ascending' else '-created'
        return queryset.order_by(expression)