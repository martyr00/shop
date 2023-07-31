import os
from typing import Optional

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
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

    @classmethod
    def get_features_list_by_id_in(cls, features_ids):
        """
        Get a list of features database entities by id.

        Arguments:
            features_ids (list): list ids features

        Returns:
             A list of features entity if it exists, as `Features`.
             Otherwise, None.
        """
        try:
            return cls.objects.filter(id__in=features_ids)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_unique_features_keys_by_category(cls, category_id: int):
        """
        Get a list of unique feature keys for products by category ID.

        Arguments:
            category_id (int): category ID of the products.

        Returns:
            A list of unique feature keys for the products in the specified category.
            Otherwise, None.
        """
        try:
            return cls.objects.filter(product__category_id=category_id).values('key').distinct()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_unique_features_value_by_keys(cls, category_id, key):
        """
        Get a list of unique feature values for products by keys.

        Arguments:
            category_id (int): category ID of the product.
            key (str): key for filtering the features.

        Returns:
            A list of unique feature values for the filtered products.
            Otherwise, None.
        """
        try:
            return Features.objects.filter(product__category_id=category_id, key=key).values('value', 'id').distinct()
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return f'{self.key}: {self.value}'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='title', unique=True)
    text = models.CharField(max_length=200, verbose_name='text', null=True, blank=True)
    price = models.BigIntegerField('price')
    description = models.CharField(max_length=500, verbose_name='description')

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    features = models.ManyToManyField(Features, )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='update_time')

    @classmethod
    def get_filtered_and_sorted_list_of_product_by_category(
            cls,
            category_id: int,
            sort_dict: str,
            sort_by: str,
            filter_params: list
    ) -> Optional[QuerySet['Product']]:
        """
        Get a filtered and sorted list of products by category ID, sorting criteria, and filter parameters.

        Arguments:
            category_id (int): category ID of the products.
            sort_dict (str): sorting direction, either '+' for ascending or '-' for descending.
            sort_by (str): The field to sort the products by.
            filter_params (list): A list of filter parameters for features.

        Returns:
            A filtered and sorted QuerySet of products matching the specified criteria.
        """
        products_list = cls.objects.filter(category_id=category_id).order_by(sort_dict + sort_by)

        if not filter_params:
            return products_list

        features_list = Features.get_features_list_by_id_in(filter_params)
        keys = features_list.values_list('key', flat=True)
        values = features_list.values_list('value', flat=True)

        for value in values:
            products_list = products_list.filter(features__key__in=keys, features__value=value)

        return products_list

    def __str__(self):
        return f'{self.id} | {self.title} | {self.category.title}'


class ProductRating(models.Model):
    class Meta:
        indexes = [
            UniqueIndex(fields=['user', 'product']),
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    grade = models.BooleanField()

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    @classmethod
    def get_count_rating_for_one_product(cls, product_id, grade=None):
        """
        Get the count of ratings for a specific product, optionally filtered by grade.

        Arguments:
            product_id (int): The ID of the product.
            grade (bool, optional): The grade to filter the ratings. Default is None.

        Returns:
            The count of ratings for the specified product and grade.
            Otherwise, None.
        """
        try:
            return cls.objects.filter(product_id=product_id, grade=grade).count()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_rating_from_user(cls, product_id, user):
        """
        Retrieves the rating of a product given by a specific user.

        Arguments:
            product_id (int): ID of the product.
            user (User): The user who gave the rating.

        Returns:
            The rating of the product given by the specified user.
            Otherwise, None.
        """
        try:
            return cls.objects.get(product_id=product_id, user=user)
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_or_update_rating(cls, grade, product_id, user):
        """
       Create or update a rating object for a product and user.

       Arguments:
           grade (int): The grade value.
           product_id (int): ID of the product.
           user (User): The user who gave the rating.

       Returns:
           True if the rating object is created or updated successfully.
           Otherwise, None.
       """
        try:
            rating_for_product_from_user = cls.objects.filter(product_id=product_id, user=user)

            if rating_for_product_from_user:
                rating_for_product_from_user.update(grade=grade)
            else:
                cls.objects.create(product_id=product_id, user=user, grade=grade)

        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_rating(cls, grade, product_id, user):
        """
        Deletes an object with the specified grade, product ID, and user.

        Arguments:
            grade (bool): The grade value.
            product_id (int): ID of the product.
            user (User): The user associated with the object.

        Returns:
            True if the object was deleted successfully.
            Otherwise, None.
        """
        try:
            cls.objects.get(product_id=product_id, user=user, grade=grade).delete()
        except cls.DoesNotExist:
            return None

    def __str__(self):
        if bool(self.grade):
            return f'Like: {self.user} | {self.product}'

        return f'Dislike {self.user} | {self.product}'


def image_upload_path(instance, filename):
    category_id = instance.product.category.id

    upload_path = os.path.join('product_images', str(category_id), filename)
    return f"image/{upload_path}"


class ProductImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=image_upload_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @classmethod
    def get_all_images_urls_for_one_product(cls, product_id):
        return ProductImage.objects.filter(product_id=product_id).values_list('image', flat=True)

    def __str__(self):
        return f'{self.title}'
