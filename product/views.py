from rest_framework import generics
from .models import Product
from .permission import IsAdminOrReadOnly
from .serializer import ProductSerializer


class GETListOfProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Response list of products"""
        category_id_from_url = self.kwargs['category_id']
        dictionary_from_id = self.request.query_params

        return get_sort_queryset(dictionary_from_id.get('sort_by'),
                                 dictionary_from_id.get('sort_dict'),
                                 get_queryset_by_category(Product.objects.all(), category_id_from_url))


def get_queryset_by_category(queryset, category_id):
    """Get list of products by category"""
    return queryset.filter(category=category_id)


def get_sort_queryset(sort_by_from_url, sort_dict_from_url, queryset):
    """Get sort list of products"""
    sort_dict = '-' if sort_dict_from_url == 'desc' else ''
    sort_by = 'title' if sort_by_from_url is None else sort_by_from_url

    return queryset.order_by(sort_dict + sort_by)
