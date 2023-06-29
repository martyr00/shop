from rest_framework import serializers
from product.models import Product, Features, Category, ProductRating


class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', )


class ProductSerializer(serializers.ModelSerializer):
    features = serializers.ManyRelatedField(child_relation=FeaturesSerializer())

    class Meta:
        model = Product
        fields = '__all__'


class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault, write_only=True)

    class Meta:
        model = ProductRating
        fields = ('user', )
