from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    ListOfProductsByCategory,
    ItemOfProducts,
    ListOfCategories,
    UniqueFeaturesProductsByCategory,
    DislikeFromUser,
    LikeFromUser,
)

urlpatterns = [
    path('category/<int:category_id>/', cache_page(60*15, cache='database_cached')(ListOfProductsByCategory.as_view())),
    path('feature/category/<int:category_id>/', UniqueFeaturesProductsByCategory.as_view()),
    path('category/', cache_page(60*15, cache='default')(ListOfCategories.as_view())),
    path('product/<int:pk>/', ItemOfProducts.as_view()),
    path('rating/<int:product_id>/like/', LikeFromUser.as_view()),
    path('rating/<int:product_id>/dislike/', DislikeFromUser.as_view()),
]
