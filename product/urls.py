from django.urls import path
from .views import GETListOfProducts, GETItemOfProduct, GETListOfFeatures, GETListOfCategories, RatingOneProduct

urlpatterns = [
    path('category/<int:category_id>/', GETListOfProducts.as_view()),
    path('product/<int:pk>/', GETItemOfProduct.as_view()),
    path('product/<int:pk>/<int:grade>', RatingOneProduct.as_view()),
    path('features/', GETListOfFeatures.as_view()),
    path('categories/', GETListOfCategories.as_view()),
]
