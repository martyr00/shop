from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from product.models import Features, Category, Product


class FeaturesModelViewGETMethodTestCase(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        """
        Set up data for tests.
        """
        self.test_features = Features.objects.create(
            key='Test key',
            value='Test value'
        )
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
        self.test_product.features.add(self.test_features)

    def test_get_unique_features_products_by_category(self):
        """
        Case: get list of unique features products by category.
        Expect: list of unique features products by category
        """
        expected_result = {
            'count': Features.objects.filter(product__category_id=self.test_category.id).count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'key': self.test_features.key,
                    'options': [
                        {
                            'value': self.test_features.value,
                            'id': self.test_features.id,
                        }
                    ]
                },
            ]
        }

        response = self.client.get(
            path=f'/api/v1/feature/category/{self.test_category.id}/',
        )

        assert HttpStatusCode.OK.value == response.status_code
        assert expected_result == response.json()

    def test_get_unique_features_products_by_category_not_found(self):
        """
        Case: get list of unique features products by category.
        Expect: not found errors' messages.
        """
        expected_result = {
            "detail": "Not found."
        }

        response = self.client.get(
            path=f'/api/v1/feature/category/{Category.objects.count()+1}/',
        )

        assert HttpStatusCode.NOT_FOUND.value == response.status_code
        assert expected_result == response.json()
