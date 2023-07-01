from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response

from .models import Product, Features, Category, ProductRating
from .permission import IsAdminOrReadOnly, IsAdminOrAuthenticatedUser
from .serializer import (
    FeaturesSerializer,
    CategorySerializer,
    ProductSerializer, ProductRatingSerializer,
)
from .filters import ProductFilter


class GetListOfProductsByCategory(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ProductFilter

    def get_queryset(self):
        """Response list of products"""
        return self.get_sort_queryset(self.get_queryset_by_category())

    def get_queryset_by_category(self):
        """Get list of products by category"""
        return Product.objects.filter(category=self.kwargs['category_id'])

    def get_sort_queryset(self, queryset):
        """Get sort list of products"""
        dictionary_from_id = self.request.query_params

        sort_dict = '-' if dictionary_from_id.get('sort_dict') == 'desc' else ''
        sort_by = 'title' if dictionary_from_id.get('sort_by') is None else dictionary_from_id.get('sort_by')

        return queryset.order_by(sort_dict + sort_by)


class GetItemOfProduct(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class GetListOfFeatures(generics.ListAPIView):
    queryset = Features.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = FeaturesSerializer


class GetListOfCategories(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = CategorySerializer


class PostRatingFromUser(generics.CreateAPIView):
    queryset = ProductRating.objects.all()
    permission_classes = [IsAdminOrAuthenticatedUser, ]
    serializer_class = ProductRatingSerializer

    def post(self, request, *args, **kwargs):
        try:
            obj, created_object = ProductRating.objects.get_or_create(
                product_id=request.data.get('product_id'),
                user=request.user,
                grade=request.data.get('grade'),
            )
            if not created_object:
                obj.delete()
                return Response(status=204)
        except IntegrityError:
            ProductRating.objects.filter(
                product_id=request.data.get('product_id'),
                user=request.user,
            ).update(
                grade=request.data.get('grade'),
            )
        return Response(status=200)
