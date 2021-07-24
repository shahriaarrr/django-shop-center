from django.core.exceptions import MultipleObjectsReturned
from django.db import models

from django.db.models import Q

# imports for slug
from django.db.models.signals import pre_save,post_save


#To display the product in active or inactive mode
class ProdctManager(models.Manager):
    def get_active_product(self):
        return self.get_queryset().filter(active=True)

    def Search(self,query):
        title_description = Q(title__icontains=query) | Q(description__icontains=query) | Q(tag__title__icontains=query)
        return self.get_queryset().filter(title_description,active=True).distinct()  # distinct -> اگر آیتم تکراری بود پاکش کن



class Product(models.Model):
    title = models.CharField(max_length=120,verbose_name="عنوان")
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to='image/',blank=True,null=True,verbose_name='تصویر')
    active = models.BooleanField(verbose_name='فعال / غیرفعال',default=False)
    
    objects = ProdctManager()
    # slug = models.SlugField(blank=True)
    # featured = models.BooleanField(default=False)

    time = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.description[:50] + '...'

    class Meta:
        verbose_name_plural = 'محصولات'  # --> for remove "s" on header page amdin
        verbose_name = 'محصولات'

# --------
# tags

class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    create_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'تگ ها'
        verbose_name = 'تگ '