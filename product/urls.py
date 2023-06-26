
from django.urls import path
from .views import GETListOfProducts

urlpatterns = [
    path('<int:category_id>/', GETListOfProducts.as_view()),
    # path('', GETListOfProducts.as_view())
]
