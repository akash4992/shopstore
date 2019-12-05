from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class CategoryType(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_list')
    categorytype = models.CharField(max_length=255)

    class Meta:
        ordering = ('categorytype',)
        verbose_name = 'categorytype'
        verbose_name_plural = 'categorytype'

    
    def __str__(self):
        return str(self.category) + ': ' + self.categorytype