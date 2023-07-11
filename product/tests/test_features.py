from django.test import TransactionTestCase
from http import HTTPStatus as HttpStatusCode

from product.models import Features, Category, Product
from product.utils import comparison_of_expected_and_result


class FeaturesModelViewGETMethodTestCase(TransactionTestCase):
    def setUp(self):
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

        comparison_of_expected_and_result(
            HttpStatusCode.OK.value,
            response.status_code,
            expected_result,
            response.json()
        )
