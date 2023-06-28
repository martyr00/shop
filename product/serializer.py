from rest_framework import serializers
from product.models import Product, Features, Category, ProductRating


class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductsListSerializer(serializers.ModelSerializer):
    features = serializers.ManyRelatedField(child_relation=FeaturesSerializer())

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product = serializers.ManyRelatedField(child_relation=ProductsListSerializer())

    class Meta:
        model = ProductRating
        fields = '__all__'