from django.db import models
from accounts.models import User
from products.models import Product
# Create your models here.


class View(models.Model):
    user = models.ManyToManyField(User)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    view_counts = models.IntegerField(default=0)

    def __str__(self):
        return "{}-{}".format(self.product,self.view_counts)
