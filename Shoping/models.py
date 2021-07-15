from django.core.exceptions import MultipleObjectsReturned
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=2)
    image = models.ImageField(upload_to='image/',blank=True,null=True)
    # featured = models.BooleanField(default=False)

    time = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.description[:50] + '...'