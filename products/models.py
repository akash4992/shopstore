from django.db import models
from django.db.models import Q
from category.models import CategoryType
from django.urls import reverse

# Create your models here.
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                  Q(description__icontains=query) |
                  Q(price__icontains=query) 
                  )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Product.objects.featured() 
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) 
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)




class Product(models.Model):
    title           = models.CharField(max_length=120)
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image           = models.ImageField(upload_to='images/') 

    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    category        = models.ForeignKey(CategoryType,on_delete=models.CASCADE)
    is_digital      = models.BooleanField(default=False) # User Library
    created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
 
    
    def __str__(self):
        return self.title


    
    
    def get_absolute_url(self):
              return reverse('products:list',kwargs={'slug': self.slug})

class Productsize(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE,related_name='details')
    value = models.CharField(max_length=50)
    stock= models.IntegerField(default=1)
    items_sold = models.IntegerField(default=0)


    def __str__(self):
        return self.value 
    class Meta:
        ordering = ('value',)

