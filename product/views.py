from http import HTTPStatus as HttpStatusCode
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from .errors import NOT_FOUND
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


class ListOfProductsByCategory(generics.ListAPIView):
    """
    A view for listing products by category.
    Only authenticated administrators have write access, while all users have read access.
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        """
        Returns the queryset of products filtered and sorted based on the provided query parameters.
        Raises NotFound exception if no products are found.
        """
        sort_dict, sort_by = self.get_query_params_for_sort()
        filter_params = self.get_query_params_for_filter()

        product_list = Product.get_filtered_and_sorted_list_of_product_by_category(
            self.kwargs['category_id'], sort_dict, sort_by, filter_params)

        if not product_list:
            raise NotFound

        return product_list

    def get_query_params_for_sort(self):
        """
        Get the sort_dict and sort_by values from the query parameters.
        Returns the sort_dict and sort_by values.
        """
        dictionary_from_id = self.request.query_params

        sort_dict = '-' if dictionary_from_id.get('sort_dict') == 'desc' else ''
        sort_by = 'title' if dictionary_from_id.get('sort_by') is None else dictionary_from_id.get('sort_by')

        return sort_dict, sort_by

    def get_query_params_for_filter(self):
        """
        Get the filter parameter values from the query parameters.
        Returns the filter parameter values as a list.
        """
        return self.request.query_params.getlist('filter') if self.request.query_params.getlist('filter') else None


class LikeFromUser(APIView):
    """
    API view for rating a product with a dislike.
    Only authenticated users have access to rate a product.
    """
    queryset = ProductRating.objects.all()
    permission_classes = [IsAdminOrAuthenticatedUser, ]
    serializer_class = ProductRatingSerializer

    def post(self, request, product_id):
        """
        Rate a product with a like and return the updated dislike count.

        Arguments:
            request (Request): a request.
            product_id (Request): a product id.

        Returns:
            updated like count
            Otherwise, incoming arguments validation errors.
        """
        if ProductRating.create_obj_or_update(True, product_id, self.request.user):
            return JsonResponse(
                {'like_count': ProductRating.get_count_rating_for_one_product(product_id, True)},
                status=HttpStatusCode.OK
            )
        return JsonResponse({'detail': NOT_FOUND}, status=HttpStatusCode.NOT_FOUND)

    def delete(self, request, product_id):
        if ProductRating.delete_obj(True, product_id, self.request.user):
            return JsonResponse(
                {'like_count': ProductRating.get_count_rating_for_one_product(product_id, True)},
                status=HttpStatusCode.OK
            )
        return JsonResponse({'detail': NOT_FOUND}, status=HttpStatusCode.NOT_FOUND)


class DislikeFromUser(APIView):
    """
    API view for rating a product with a dislike.
    Only authenticated users have access to rate a product.
    """
    queryset = ProductRating.objects.all()
    permission_classes = [IsAdminOrAuthenticatedUser, ]
    serializer_class = ProductRatingSerializer

    def post(self, request, product_id):
        """
        Rate a product with a dislike and return the updated dislike count.

         Arguments:
            request (Request): a request.
            product_id (Request): a product id.

        Returns:
            updated dislike count
            Otherwise, incoming arguments validation errors.
        """
        if ProductRating.create_obj_or_update(False, product_id, self.request.user):
            return JsonResponse(
                {'dislike_count': ProductRating.get_count_rating_for_one_product(product_id, False)},
                status=HttpStatusCode.OK
            )
        return JsonResponse({'detail': NOT_FOUND}, status=HttpStatusCode.NOT_FOUND)

    def delete(self, request, product_id):
        if ProductRating.delete_obj(False, product_id, self.request.user):
            return JsonResponse(
                {'dislike_count': ProductRating.get_count_rating_for_one_product(product_id, False)},
                status=HttpStatusCode.OK
            )
        return JsonResponse({'detail': NOT_FOUND}, status=HttpStatusCode.NOT_FOUND)


class ItemOfProducts(generics.RetrieveAPIView):
    """
    A view for retrieving a single product item.
    Only authenticated administrators have write access, while all users have read access.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class ListOfCategories(generics.ListAPIView):
    """
    A view for listing categories.
    Only authenticated administrators have write access, while all users have read access.
    """
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = CategorySerializer


class UniqueFeaturesProductsByCategory(generics.ListAPIView):
    """
    A view for retrieving unique keys of features by products in a specific category.
    Only authenticated administrators have write access, while all users have read access.
    """
    queryset = Features.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = FeaturesSerializer

    def get_queryset(self):
        """
        Returns a queryset of unique feature keys by category.
        Raises NotFound exception if no features are found.
        """
        result_queryset = Features.get_unique_features_keys_by_category(self.kwargs['category_id'])
        if result_queryset:
            return result_queryset
        raise NotFound
