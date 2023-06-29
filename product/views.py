from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions


from .models import Product, Features, Category, ProductRating
from .permission import IsAdminOrReadOnly
from .serializer import FeaturesSerializer, CategorySerializer, ProductSerializer, ProductRatingSerializer
from .filters import ProductFilter


class GETListOfProducts(generics.ListAPIView):
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


class GETItemOfProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class GETListOfFeatures(generics.ListAPIView):
    queryset = Features.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = FeaturesSerializer


class GETListOfCategories(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = CategorySerializer


class RatingOneProduct(generics.ListCreateAPIView):
    queryset = ProductRating.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ProductRatingSerializer

    def get_queryset(self):
        product = ProductRating.objects.filter(product=self.kwargs.get('pk'))
        return product.filter(grade=bool(self.kwargs.get('grade')))
