import os

from django.core.files import File
from django.test import TransactionTestCase

from product.models import Category, Product, ProductImage


class ProductModelViewGETMethodTestCase(TransactionTestCase):
    def setUp(self):
        self.test_category = Category.objects.create(
            title='Test category'
        )
        self.test_product = Product.objects.create(
            title='Test product title',
            text=None,
            price=500,
            description='test product description',
            category=self.test_category,
        )
        self.test_product_image = ProductImage.objects.create(
            title='test',
            image=File(open('test_image1.png', 'rb')),
            product=self.test_product
        )

    def test_check_product_image_in_db(self):
        """"""
        print(self.test_product_image.image)
        assert ProductImage.objects.count() == 1
        assert self.test_product_image.title == 'test'
        assert self.test_product_image.image == 'image/product_images/Test category/test_image1.png'
        assert self.test_product_image.product == self.test_product

        os.remove('media/image/product_images/Test category/test_image1.png')

    def test_record_product_image_to_db(self):
        """"""
        ProductImage.objects.create(
            title='test2',
            image=File(open('test_image2.png', 'rb')),
            product=self.test_product
        )

        image2 = ProductImage.objects.get(pk=3)

        assert ProductImage.objects.count() == 2
        assert image2.title == 'test2'
        assert image2.image == 'image/product_images/Test category/test_image2.png'
        assert image2.product == self.test_product

        os.remove('media/image/product_images/Test category/test_image1.png')
        os.remove('media/image/product_images/Test category/test_image2.png')
