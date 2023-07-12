import json

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Category, Product


class UserModelViewPOSTMethodTestCase(TransactionTestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_pass'

    def test_create_user(self):
        pass
