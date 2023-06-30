from django.urls import path
from .views import GetListOfProducts, GetItemOfProduct, GetListOfFeatures, GetListOfCategories, PostRatingFromUser

urlpatterns = [
    path('category/<int:category_id>/', GetListOfProducts.as_view()),
    path('product/<int:pk>/', GetItemOfProduct.as_view()),
    path('product/<int:pk>/<int:grade>', PostRatingFromUser.as_view()),
    path('features/', GetListOfFeatures.as_view()),
    path('categories/', GetListOfCategories.as_view()),
]
