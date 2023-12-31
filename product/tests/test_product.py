from django.contrib.auth.models import User
from django.core.files import File
from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Category, Product, Features, ProductRating, ProductImage


class ProductModelViewGETMethodTestCase(TransactionTestCase):
    """
    Product collection view get method test case implementation.
    """

    reset_sequences = True

    def setUp(self):
        """
        Set up data for tests.
        """
        self.test_category = Category.objects.create(
            title='Test Category'
        )
        self.test_features = Features.objects.create(
            key='Test key',
            value='Test value'
        )
        self.test_product_rating = ProductRating.objects
        self.test_user = User.objects.create(
            username='test_user',
            password='test_password'
        )
        self.test_product = Product.objects.create(
            title='title test',
            text=None,
            price=500,
            description='test description test',
            category=self.test_category,
        )
        self.test_product.features.add(self.test_features)
        self.test_product_image = ProductImage.objects.create(
            title='test',
            image=File(open('test_image1.png', 'rb')),
            product=self.test_product
        )

    def get_main_fields_for_expected_result_product(self):
        """Get main fields for expected_result"""
        return {
            'id': self.test_product.id,
            'title': self.test_product.title,
            'price': self.test_product.price,
            'category': self.test_product.category.title,
            'category_id': self.test_product.category.id,
            'features': [{
                'id': self.test_features.id,
                'key': self.test_features.key,
                'value': self.test_features.value
            }],
            'media': [
                f'/media/{self.test_product_image.image}'
            ]
        }

    def get_expected_fields_for_one_product(self, user_rating, like_count, dislike_count):
        """Get main field and fields for one product"""
        return {
            **self.get_main_fields_for_expected_result_product(),
            'text': self.test_product.text,
            'description': self.test_product.description,
            'rating': {
                'like_count': like_count,
                'dislike_count': dislike_count,
                'current_user_rating': user_rating,
            }
        }

    def test_get_list_of_product_by_category(self):
        """
        Case: get list of product by category.
        Expect: returned list of product.
        """
        expected_result = {
            'count': Product.objects.count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    **self.get_main_fields_for_expected_result_product()
                },
            ]
        }

        response = self.client.get(
            path='/api/v1/category/1/',
        )

        assert HttpStatusCode.OK.value == response.status_code
        assert expected_result == response.json()

    def test_get_list_of_product_by_category_not_found(self):
        """
        Case: get list of product by category with category id out of scope
        Expect: not found errors' messages.
        """
        expected_result = {
            "detail": "Not found."
        }

        response = self.client.get(
            path=f'/api/v1/category/{Category.objects.count()+1}/',
        )

        assert HttpStatusCode.NOT_FOUND.value == response.status_code
        assert expected_result == response.json()

    def test_get_product_no_rating_from_user(self):
        """
        Case: get product with rating.
        Expect: returned product no rating from user.
        """
        expected_result = self.get_expected_fields_for_one_product(
            user_rating=None,
            like_count=0,
            dislike_count=0
        )

        response = self.client.get(
            path=f'/api/v1/product/{self.test_product.id}/',
        )

        assert HttpStatusCode.OK.value == response.status_code
        assert expected_result == response.json()

    def test_get_product_with_like_from_user(self):
        """
        Case: get product with rating.
        Expect: returned product with like from user.
        """
        expected_result = {
            **self.get_expected_fields_for_one_product(
                user_rating='like',
                like_count=1,
                dislike_count=0
            )
        }

        ProductRating.objects.create(product=self.test_product, user=self.test_user, grade=True)

        response = self.client.get(
            path=f'/api/v1/product/{self.test_product.id}/',
            headers={"Authorization": "Bearer " + str(RefreshToken.for_user(self.test_user).access_token)}
        )

        assert HttpStatusCode.OK.value == response.status_code
        assert expected_result == response.json()

    def test_get_product_with_dislike_from_user(self):
        """
        Case: get product with rating.
        Expect: returned product with dislike from user.
        """
        expected_result = {
                **self.get_expected_fields_for_one_product(
                    user_rating='dislike',
                    like_count=0,
                    dislike_count=1,
                )
            }

        ProductRating.objects.create(product=self.test_product, user=self.test_user, grade=False)

        response = self.client.get(
            path=f'/api/v1/product/{self.test_product.id}/',
            headers={"Authorization": "Bearer " + str(RefreshToken.for_user(self.test_user).access_token)}
        )

        assert HttpStatusCode.OK.value == response.status_code
        assert expected_result == response.json()

    def test_get_product_not_found(self):
        """
        Case: get product with product id out of scope
        Expect: not found errors' messages.
        """
        expected_result = {
            "detail": "Not found."
        }

        response = self.client.get(
            path=f'/api/v1/product/{Product.objects.count()+1}/',
        )

        assert HttpStatusCode.NOT_FOUND.value == response.status_code
        assert expected_result == response.json()

    def test_get_product_with_query_params(self):
        """
        Case: get list product with the features.
        Expect: list product filtered by features .
        """

        test_features_in_product = Product.objects.create(
            title='title test2',
            text=None,
            price=400,
            description='test description test',
            category=self.test_category,
        )

        test_features_in_product.features.add(Features.objects.create(
            key='Test key 2',
            value='Test value 2'
        ))
        expected_result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 2,
                    'title': 'title test2',
                    'price': 400,
                    'category': 'Test Category',
                    'category_id': 1,
                    'features': [
                        {
                            'id': 2,
                            'key': 'Test key 2',
                            'value': 'Test value 2'
                        }
                    ],
                    'media': [],
                },
            ]
        }

        response = self.client.get(
            path=f'/api/v1/category/{self.test_category.id}/?filter=2',
        )

        assert HttpStatusCode.OK.value == response.status_code
        assert expected_result == response.json()

    def tearDown(self):
        """
        Method to clean up resources after each test.
        """
        self.test_product_image.image.delete()
        self.test_product_image.delete()
        self.test_product.delete()
        self.test_category.delete()
