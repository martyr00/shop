import os

from django.core.files import File
from django.test import TransactionTestCase

from product.models import Category, Product, ProductImage


class ProductModelViewGETMethodTestCase(TransactionTestCase):
    def setUp(self):
        """
        Set up data for tests.
        """
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
        """
        Case: Retrieving a `ProductImage` object from the database and comparing its attributes with the original.
        Expect:
            - The number of `ProductImage` objects in the database should be equal to 1.
            - The `title`, `image`, and `product` attributes of the retrieved object should match the original object.
        """
        image1_from_db = ProductImage.objects.get(pk=self.test_product_image.id)

        assert ProductImage.objects.count() == 1
        assert self.test_product_image.title == image1_from_db.title
        assert self.test_product_image.image == image1_from_db.image
        assert self.test_product_image.product == image1_from_db.product

    def test_record_product_image_to_db(self):
        """
        Case: Creating a new `ProductImage` object and saving it to the database.
        Expect: The `ProductImage` object should be successfully created and saved to the database.
        """
        image2 = ProductImage.objects.create(
            title='test2',
            image=File(open('test_image2.png', 'rb')),
            product=self.test_product
        )

        assert ProductImage.objects.filter(pk=image2.id).exists()

        image2.delete()

        assert not ProductImage.objects.filter(pk=image2.id).exists()

        os.remove(image2.image.path)

    def tearDown(self):
        """
        Method to clean up resources after each test.
        """
        self.test_product_image.image.delete()
        self.test_product_image.delete()
        self.test_product.delete()
        self.test_category.delete()
