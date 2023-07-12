import json

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Category, Product, ProductRating
from product.utils import comparison_of_expected_and_result


class ProductRatingModelViewPOSTMethodTestCase(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        self.test_category = Category.objects.create(
            title='Test title'
        )
        self.test_product = Product.objects.create(
            title='title test',
            text=None,
            price=500,
            description='test description test',
            category=self.test_category,
        )
        self.test_user = User.objects.create(
            username='test_user',
            password='test_password'
        )
        self.grade_like = True
        self.grade_dislike = False
        self.count_like = ProductRating.objects.filter(
            product_id=self.test_product.id,
            grade=self.grade_like
        ).count()
        self.count_dislike = ProductRating.objects.filter(
            product_id=self.test_product.id,
            grade=self.grade_dislike
        ).count()
        self.data_post_like = {
            'product_id': self.test_product.id,
            'grade': 'like'
        }
        self.data_post_dislike = {
            'product_id': self.test_product.id,
            'grade': 'dislike'
        }

    def test_record_user_rating_like(self):
        """
        Case: record like from user
        Expect: returned count like + user's like
        """
        expected_result = {
            'like_count': self.count_like + 1
        }

        response = self.client.post(
            path='/api/v1/rating/',
            data=json.dumps(self.data_post_like),
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + str(RefreshToken.for_user(self.test_user).access_token)}
        )

        comparison_of_expected_and_result(
            HttpStatusCode.OK.value,
            response.status_code,
            expected_result,
            response.json()
        )

    def test_remove_user_rating_like(self):
        """
        Case: remove like from user
        Expect: returned count like - user's like
        """

        expected_result = {
            'like_count': self.count_like
        }

        ProductRating.objects.create(
            product_id=self.test_product.id,
            user=self.test_user,
            grade=self.grade_like
        )

        response = self.client.post(
            path='/api/v1/rating/',
            data=json.dumps(self.data_post_like),
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + str(RefreshToken.for_user(self.test_user).access_token)}
        )

        comparison_of_expected_and_result(
            HttpStatusCode.OK.value,
            response.status_code,
            expected_result,
            response.json()
        )

    def test_swap_user_rating_from_like_to_dislike(self):
        """
        Case: swap like with dislike
        Expect: returned count dislike + user's dislike
        """

        expected_result = {
            'dislike_count': self.count_dislike + 1
        }

        ProductRating.objects.create(
            product_id=self.test_product.id,
            user=self.test_user,
            grade=self.grade_like,
        )

        response = self.client.post(
            path='/api/v1/rating/',
            data=json.dumps(self.data_post_dislike),
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + str(RefreshToken.for_user(self.test_user).access_token)}
        )

        comparison_of_expected_and_result(
            HttpStatusCode.OK.value,
            response.status_code,
            expected_result,
            response.json()
        )

    def test_record_user_rating_unauthorized(self):
        """
        Case: check user's access token
        Expect: returned error's message unauthorized
        """
        response = self.client.post(
            path='/api/v1/rating/',
            data=json.dumps(self.data_post_like),
            content_type='application/json',
        )
        assert HttpStatusCode.UNAUTHORIZED.value == response.status_code
