from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from product.models import Category


class CategoryModelViewGetMethodTestCase(TransactionTestCase):
    """
   Category collection view get method test case implementation.
   """

    databases = {'default'}
    reset_sequences = True
    serialized_rollback = True

    def setUp(self):
        """
        Set up data for tests.
        """
        self.test_category = Category.objects.create(
            title='Test Category'
        )

    def test_get_list_of_category(self):
        """
        Case: get list of category.
        Expect: returned list of category.
        """
        expected_result = {
            'count': Category.objects.count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'title': self.test_category.title,
                    'id': self.test_category.id
                },
            ]
        }

        response = self.client.get(
            '/api/v1/category/',
            headers={'accept': 'application/json'},
        )

        assert HttpStatusCode.OK.value == response.status_code
        assert expected_result == response.json()
        assert Category.objects.filter(id=self.test_category.id)
