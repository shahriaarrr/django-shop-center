from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__','slug','title','price']
    list_filter = ['title','price']
    

    class Meta:
        model = Product


admin.site.register(Product,ProductAdmin)
