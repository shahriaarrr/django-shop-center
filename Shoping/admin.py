from django.contrib import admin

from .models import Product,Tag,Category,Slider,Gallery,ContactUsModel


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__','title','price','active',]
    list_filter = ['title','price']
    

    class Meta:
        model = Product


class galleryAdmin(admin.ModelAdmin):
    list_display = ['title','product']

class contact_us(admin.ModelAdmin):
    list_display = ['full_name','is_read']
    list_filter = ['is_read']


admin.site.register(Product,ProductAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Slider)
admin.site.register(Gallery,galleryAdmin)
admin.site.register(ContactUsModel,contact_us)




