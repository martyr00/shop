from django.urls import path
from .views import (
    GetListOfProductsByCategory,
    GetItemOfProduct,
    GetListOfCategories,
    PostRatingFromUser,
    GetUniqueFeaturesProductsByCategory,
)

urlpatterns = [
    path('category/<int:category_id>/', GetListOfProductsByCategory.as_view()),
    path('feature/category/<int:category_id>/', GetUniqueFeaturesProductsByCategory.as_view()),
    path('category/', GetListOfCategories.as_view()),
    path('product/<int:pk>/', GetItemOfProduct.as_view()),
    path('rating/', PostRatingFromUser.as_view()),
]
