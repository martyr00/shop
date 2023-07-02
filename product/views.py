from django.db import IntegrityError
from django.http import Http404
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


class GetListOfProductsByCategory(generics.ListAPIView):
    """Response list of products by category id"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ProductFilter

    def get_queryset(self):
        """Response queryset"""
        return self.get_filtered_queryset(self.get_sort_queryset(self.get_queryset_by_category()))

    def get_queryset_by_category(self):
        """Get queryset by category"""
        if Product.objects.filter(category=self.kwargs['category_id']):
            return Product.objects.filter(category=self.kwargs['category_id'])
        raise NotFound

    def get_sort_queryset(self, queryset):
        """Get sort queryset"""
        dictionary_from_id = self.request.query_params

        sort_dict = '-' if dictionary_from_id.get('sort_dict') == 'desc' else ''
        sort_by = 'title' if dictionary_from_id.get('sort_by') is None else dictionary_from_id.get('sort_by')

        return queryset.order_by(sort_dict + sort_by)

    def get_filtered_queryset(self, queryset):
        keys = self.request.query_params.get('key').split(',') if self.request.query_params.get('key') else None
        values = self.request.query_params.get('value').split(',') if self.request.query_params.get('value') else None

        if not keys and not values or len(keys) != len(values):
            return queryset
#
        for ele in range(len(keys)):
            queryset = queryset.filter(features__key=keys[ele], features__value=values[ele])

        return queryset


class PostRatingFromUser(generics.CreateAPIView):
    """Rate the product"""
    queryset = ProductRating.objects.all()
    permission_classes = [IsAdminOrAuthenticatedUser, ]
    serializer_class = ProductRatingSerializer

    def post(self, request, *args, **kwargs):
        """record user rating in database"""
        grade = True if request.data.get('grade') == 'like' else False
        try:
            obj, created_object = ProductRating.objects.get_or_create(
                product_id=request.data.get('product_id'),
                user=request.user,
                grade=grade,
            )
            if not created_object:
                obj.delete()
                return Response(status=204)
        except IntegrityError:
            ProductRating.objects.filter(
                product_id=request.data.get('product_id'),
                user=request.user,
            ).update(
                grade=grade,
            )
        return Response(status=200)


class GetItemOfProduct(generics.RetrieveAPIView):
    """Get one product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class GetListOfCategories(generics.ListAPIView):
    """Get list of category"""
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = CategorySerializer


class GetUniqueFeaturesProductsByCategory(generics.ListAPIView):
    """Get unique key features of products of one category"""
    queryset = Features.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = FeaturesSerializer

    def get_queryset(self):
        """response unique features.key dict by category"""
        return Features.objects.filter(
            product__category_id=self.kwargs['category_id']
        ).distinct().values(
            'key',
        ).distinct()
