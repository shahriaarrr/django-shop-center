from posixpath import splitext
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

from django.contrib.auth.models import User

from django.db.models import Q

# imports for slug
from django.db.models.signals import pre_save,post_save

# set name image
import os
# for sliders
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.id}-{instance.title}{ext}'
    return f'sliders/{final_name}'


# for Gallery
def get_filename_Gallery_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_Gallery_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.id}-{instance.title}{ext}'
    return f'gallery/{final_name}'




#To display the product in active or inactive mode
class ProdctManager(models.Manager):
    def get_active_product(self):
        return self.get_queryset().filter(active=True)

    def get_category(self,categoty_name):
        return self.get_queryset().filter(categories__name__iexact=categoty_name,active=True)

    def Search(self,query):
        title_description = Q(title__icontains=query) | Q(description__icontains=query) | Q(tag__title__icontains=query)  # search with tags
        return self.get_queryset().filter(title_description,active=True).distinct()  # distinct -> اگر آیتم تکراری بود پاکش کن


class Category(models.Model):
    title = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'دسته بندی ها'
        verbose_name = 'دسته بندی'
    

class Product(models.Model):
    title = models.CharField(max_length=120,verbose_name="عنوان")
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to='image/',blank=True,null=True,verbose_name='تصویر')
    active = models.BooleanField(verbose_name='فعال / غیرفعال',default=False)
    categories = models.ManyToManyField(Category,blank=True,verbose_name='دسته بندی ها')
    
    objects = ProdctManager()
    # slug = models.SlugField(blank=True)
    # featured = models.BooleanField(default=False)

    time = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.description[:50] + '...'

    def header(self):
        return self.title[:13] + '...'

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
        verbose_name = 'تگ'




class Slider(models.Model):
    title = models.CharField(max_length=150)
    link = models.URLField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image_path,blank=True,null=True,verbose_name='تصویر')
    
    def __str__(self):
        return self.title

    
# Gallery for product
class Gallery(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_image_Gallery_path,verbose_name='تصویر')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
 
    def __str__(self):
        return self.title



class ContactUsModel(models.Model):
    full_name = models.CharField(max_length=150,verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=150,verbose_name='ایمیل')
    text = models.TextField(verbose_name='متن پیام')
    is_read = models.BooleanField(verbose_name='خوانده شده / نشده',default=False)


    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'تماس های کاربران'
        verbose_name = 'تماس با ما '



class AboutUs(models.Model):
    text = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name_plural = 'درباره ما'
        verbose_name = 'درباره ما'


# order
class Order(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    is_paid = models.BooleanField(verbose_name='پرداخت شده / نشده')
    payment_date = models.DateTimeField(blank=True,null=True,verbose_name='تاریخ پرداخت')

    def __str__(self):
        return str(self.owner)
        
    class Meta:
        verbose_name_plural = 'سبد های خرید کاربران'
        verbose_name = 'سبد خرید'




class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سبد خرید')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    price = models.IntegerField(verbose_name='قیمت محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name_plural = 'اصلاعات جزئیات محصولات'
        verbose_name = 'جزئیات محصول'

    