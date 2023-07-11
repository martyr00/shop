from django.contrib.auth.models import User
from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Category, Product, Features, ProductRating
from product.utils import comparison_of_expected_and_result


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
        }

    def get_expected_fields_for_one_product(self, like, dislike, like_count, dislike_count):
        """Get main field and fields for one product"""
        return {
            **self.get_main_fields_for_expected_result_product(),
            'text': self.test_product.text,
            'description': self.test_product.description,
            'rating': {
                'like_count': like_count,
                'dislike_count': dislike_count,
                'current_user_likes': like,
                'current_user_dislikes': dislike
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

        comparison_of_expected_and_result(
            HttpStatusCode.OK.value,
            response.status_code,
            expected_result,
            response.json()
        )

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

        comparison_of_expected_and_result(
            HttpStatusCode.NOT_FOUND.value,
            response.status_code,
            expected_result,
            response.json()
        )

    def test_get_product_no_rating_from_user(self):
        """
        Case: get product with rating.
        Expect: returned product no rating from user.
        """
        expected_result = self.get_expected_fields_for_one_product(
            like=False,
            dislike=False,
            like_count=0,
            dislike_count=0
        )

        response = self.client.get(
            path=f'/api/v1/product/{self.test_product.id}/',
        )

        comparison_of_expected_and_result(
            HttpStatusCode.OK.value,
            response.status_code,
            expected_result,
            response.json()
        )

    def test_get_product_with_like_from_user(self):
        """
        Case: get product with rating.
        Expect: returned product with like from user.
        """
        expected_result = {
            **self.get_expected_fields_for_one_product(
                like=True,
                dislike=False,
                like_count=1,
                dislike_count=0
            )
        }

        ProductRating.objects.create(product=self.test_product, user=self.test_user, grade=True)

        response = self.client.get(
            path=f'/api/v1/product/{self.test_product.id}/',
            headers={"Authorization": "Bearer " + str(RefreshToken.for_user(self.test_user).access_token)}
        )

        comparison_of_expected_and_result(
                HttpStatusCode.OK.value,
                response.status_code,
                expected_result,
                response.json()
            )

    def test_get_product_with_dislike_from_user(self):
        """
        Case: get product with rating.
        Expect: returned product with dislike from user.
        """
        expected_result = {
                **self.get_expected_fields_for_one_product(
                    like=False,
                    dislike=True,
                    like_count=0,
                    dislike_count=1,
                )
            }

        ProductRating.objects.create(product=self.test_product, user=self.test_user, grade=False)

        response = self.client.get(
            path=f'/api/v1/product/{self.test_product.id}/',
            headers={"Authorization": "Bearer " + str(RefreshToken.for_user(self.test_user).access_token)}
        )

        comparison_of_expected_and_result(
                HttpStatusCode.OK.value,
                response.status_code,
                expected_result,
                response.json()
            )

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

        comparison_of_expected_and_result(
            HttpStatusCode.NOT_FOUND.value,
            response.status_code,
            expected_result,
            response.json()
        )
