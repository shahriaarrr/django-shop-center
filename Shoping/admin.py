from django.contrib import admin

from .models import Product,Tag,Category,Slider


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__','title','price','active',]
    list_filter = ['title','price']
    

    class Meta:
        model = Product


admin.site.register(Product,ProductAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Slider)


