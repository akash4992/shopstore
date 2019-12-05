from django.shortcuts import render
from django.views.generic import ListView
from .models import Category,CategoryType
from products.models import Product

# Create your views here.
def category(request):
    message = "Men Woman  kids"
    context = {
        "data":message
    }
    return render (request,'category/category_list.html',context)



class CategoryListView(ListView):
    template_name = 'category/category_list.html'
    model = Category

    
class CategorytypeListView(ListView):
    template_name = 'category/category_type.html'
    model = CategoryType

    def get_queryset(self, *args, **kwargs):
        cat_id = Category.objects.filter(id=self.kwargs['pk']).first()
        return CategoryType.objects.filter(category__name= cat_id)

class ProductListCategory(ListView):
    template_name = 'category/product_category.html'
    model = Product

    def get_queryset(self, *args, **kwargs):
        cat_id = CategoryType.objects.filter(id=self.kwargs['pk']).first()
       
        return Product.objects.filter(category = cat_id)
