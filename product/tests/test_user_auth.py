import json

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from product.utils import comparison_of_expected_and_result


class UserModelViewPOSTMethodTestCase(TransactionTestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='main_test',
            password='main_test_pass'
        )
        self.username = 'test'
        self.password = 'test_pass'

    def test_create_user(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(
            path='/api/v1/user/registration/',
            data=json.dumps(data),
            content_type='application/json',
        )
        assert HttpStatusCode.CREATED.value == response.status_code
        assert isinstance(response.json().get('refresh'), str)
        assert isinstance(response.json().get('access'), str)

    def test_create_user_username_already_exists(self):
        expected_result = {
            "username": ["A user with that username already exists."]
        }
        data_with_username_already_exists = {
            'username': 'main_test',
            'password': 'main_test_pass'
        }
        response = self.client.post(
            path='/api/v1/user/registration/',
            data=json.dumps(data_with_username_already_exists),
            content_type='application/json',
        )

        comparison_of_expected_and_result(
            HttpStatusCode.BAD_REQUEST.value,
            response.status_code,
            expected_result,
            response.json()
        )
