from http import HTTPStatus as HttpStatusCode
from django.db import IntegrityError
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import (
    Product,
    Category,
    ProductRating, Features,
)
from .permission import (
    IsAdminOrReadOnly,
    IsAdminOrAuthenticatedUser,
)
from .serializer import (
    CategorySerializer,
    ProductListSerializer, ProductRatingSerializer, ProductSerializer, FeaturesSerializer,
)
from .filters import ProductFilter


class ListOfProductsByCategory(generics.ListAPIView):
    """Response filtered list of products by category_id and features and sorted"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ProductFilter

    def get_queryset(self):
        """Response queryset"""
        return self.get_filtered_queryset(self.get_sort_queryset(self.get_queryset_by_category()))

    def get_queryset_by_category(self):
        """Get queryset filtered by category"""
        product_list_by_category = Product.objects.filter(category=self.kwargs['category_id'])
        if product_list_by_category:
            return product_list_by_category
        raise NotFound

    def get_sort_queryset(self, queryset):
        """Get sort queryset"""
        dictionary_from_id = self.request.query_params

        sort_dict = '-' if dictionary_from_id.get('sort_dict') == 'desc' else ''
        sort_by = 'title' if dictionary_from_id.get('sort_by') is None else dictionary_from_id.get('sort_by')

        return queryset.order_by(sort_dict + sort_by)

    def get_filtered_queryset(self, queryset):
        """Get queryset filtered by features_id in query_params"""
        filters = self.request.query_params.getlist('filter') if self.request.query_params.getlist('filter') else None

        if not filters:
            return queryset

        features = Features.objects.filter(id__in=filters)

        keys = features.values_list('key', flat=True)
        values = features.values_list('value', flat=True)

        for ele in range(len(values)):
            queryset = queryset.filter(features__key__in=keys, features__value=values[ele])

        return queryset


class RatingFromUser(generics.CreateAPIView):
    """Rate the product"""
    queryset = ProductRating.objects.all()
    permission_classes = [IsAdminOrAuthenticatedUser, ]
    serializer_class = ProductRatingSerializer

    def post(self, request, *args, **kwargs):
        """Record user rating in database"""
        grade = True if request.data.get('grade') == 'like' else False
        enum_grade = 'like' if grade else 'dislike'
        product_id = request.data.get('product_id')
        filter_product_rating_in_product_by_grade = ProductRating.objects.filter(product_id=product_id,grade=grade)
        if not product_id:
            return JsonResponse({'detail': 'Bad request.'}, status=HttpStatusCode.BAD_REQUEST)

        try:
            obj, created_object = ProductRating.objects.get_or_create(
                product_id=product_id,
                user=request.user,
                grade=grade,
            )
            if not created_object:
                obj.delete()
        except IntegrityError:
            ProductRating.objects.filter(
                product_id=product_id,
                user=request.user,
            ).update(
                grade=grade,
            )
        return JsonResponse(
            {f'{enum_grade}_count': filter_product_rating_in_product_by_grade.count()},
            status=HttpStatusCode.OK)


class ItemOfProducts(generics.RetrieveAPIView):
    """Get one product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class ListOfCategories(generics.ListAPIView):
    """Get filtered queryset  category"""
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = CategorySerializer


class UniqueFeaturesProductsByCategory(generics.ListAPIView):
    """Get unique keys of features by products in one category"""
    queryset = Features.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = FeaturesSerializer

    def get_queryset(self):
        """Response unique features keys dict by category"""
        result_queryset = Features.objects.filter(
            product__category_id=self.kwargs['category_id']
        ).distinct().values(
            'key',
        ).distinct()
        if result_queryset:
            return result_queryset
        raise NotFound
