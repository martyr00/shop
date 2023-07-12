import json

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Category, Product


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

    def test_record_user_rating_like(self):
        data = {
            'product_id': self.test_product.id,
            'grade': 'like'
        }
        response = self.client.post(
            path='/api/v1/rating/',
            data=json.dumps(data),
            content_type='application/json',
            headers={"Authorization": "Bearer " + str(RefreshToken.for_user(self.test_user).access_token)}
        )
        print(response.status_code)
        print(response)
        assert HttpStatusCode.OK.value == response.status_code

    def test_remove_user_rating_like(self):
        pass

    def test_record_user_rating_dislike(self):
        pass

    def test_remove_user_rating_dislike(self):
        pass

    def test_swap_user_rating_from_like_to_dislike(self):
        pass

    def test_swap_user_rating_from_dislike_to_like(self):
        pass

    def test_record_user_rating_product_not_found(self):
        pass

    def test_record_user_rating_with_invalid_incoming_arguments_product_id(self):
        pass

    def test_record_user_rating_with_invalid_incoming_arguments_grade(self):
        pass

    def test_record_user_rating_unauthorized(self):
        pass
