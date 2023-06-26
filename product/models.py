from django.contrib.auth.models import User
from django.db import models
from psqlextra.indexes import UniqueIndex


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='title', unique=True)

    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Features(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.key}: {self.value}'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='title', unique=True)
    text = models.CharField(max_length=200, verbose_name='text', null=True, blank=True)
    price = models.CharField(max_length=50, verbose_name='price')
    description = models.CharField(max_length=500, verbose_name='description')

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    features = models.ManyToManyField(Features, )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='update_time')

    def __str__(self):
        return f'{self.title} | {self.category.title}'


class ProductRating(models.Model):
    class Meta:
        indexes = [
            UniqueIndex(fields=['user', 'product']),
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    grade = models.BooleanField()

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    def __str__(self):
        if bool(self.grade):
            return f'Like: {self.user} | {self.product}'

        return f'Dislike {self.user} | {self.product}'
