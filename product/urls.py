from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    GetListOfProductsByCategory,
    GetItemOfProduct,
    GetListOfCategories,
    PostRatingFromUser,
    GetUniqueFeaturesProductsByCategory,
)

urlpatterns = [
    path('category/<int:category_id>/', cache_page(60*15, cache='database_cached')(GetListOfProductsByCategory.as_view())),
    path('feature/category/<int:category_id>/', GetUniqueFeaturesProductsByCategory.as_view()),
    path('category/', cache_page(60*15, cache='default')(GetListOfCategories.as_view())),
    path('product/<int:pk>/', GetItemOfProduct.as_view()),
    path('rating/', PostRatingFromUser.as_view()),
]
