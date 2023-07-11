from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    ListOfProductsByCategory,
    ItemOfProducts,
    ListOfCategories,
    RatingFromUser,
    UniqueFeaturesProductsByCategory,
)

urlpatterns = [
    path('category/<int:category_id>/', cache_page(60*15, cache='database_cached')(ListOfProductsByCategory.as_view())),
    path('feature/category/<int:category_id>/', UniqueFeaturesProductsByCategory.as_view()),
    path('category/', cache_page(60*15, cache='default')(ListOfCategories.as_view())),
    path('product/<int:pk>/', ItemOfProducts.as_view()),
    path('rating/', RatingFromUser.as_view()),
]
