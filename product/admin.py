from django.contrib import admin

from product.models import ProductRating, Product, Category, Features

# Register your models here.

admin.site.register(ProductRating)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Features)
