from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
# Create your views here.
class SearchProductListView(ListView):
    '''Search  for  the products'''
    template_name = "search/search.html"
    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context
    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q',None)
        if query is not None:
            return Product.objects.filter(Q(title__icontains=query) |
                  Q(description__icontains=query) |
                  Q(price__icontains=query)
                  )
        return Product.objects.featured()

       