from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Product
from .permission import IsAdminOrReadOnly
from .serializer import ProductSerializer
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

        sort_dict = '-' if dictionary_from_id.get('sort_by') == 'desc' else ''
        sort_by = 'title' if dictionary_from_id.get('sort_dict') is None else dictionary_from_id.get('sort_dict')

        return queryset.order_by(sort_dict + sort_by)
